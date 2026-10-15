#!/usr/bin/env node
/**
 * Data Boundary Guard — the Node original
 *
 * NOT THE DEFAULT. Since 2026-10-14 the settings templates wire
 * data-boundary-guard.py, the Python version beside this file, because it is
 * the one that has actually been executed and proven (see ../DATA-BOUNDARY.md).
 * This file has never been run: the machine the factory is built on has no
 * Node. Reading it shows three things the Python version does differently:
 *   - It keeps only the first 1 MiB of stdin (MAX_STDIN below), so a Write or
 *     Edit whose JSON is larger fails to parse and is allowed unchecked.
 *   - Its Bash rule treats any word matching a secret pattern as a path, so it
 *     blocks routine commands such as `git config user.name`; the Python
 *     version counts a plain word only when a file by that name exists.
 *   - It blocks commands that use a project's gitignored tool folders
 *     (.venv/bin/, venv/bin/, node_modules/.bin/), so it cannot run a Python
 *     project's own tests; the Python version allows those in commands.
 * Wire this one only on a machine with Node, and only after its armed check.
 *
 * Authored for KEEL FACTORY — not part of ECC. ECC ships nothing that plays
 * this role (checked: no hook there respects .gitignore or blocks a
 * secret-shaped path by default; the closest thing, insaits-security-wrapper.js,
 * is an opt-in wrapper around an external Python tool, not a default-on guard).
 * This hook exists because the factory is meant to be usable against
 * production systems without a human having to remember to protect anything
 * by hand.
 *
 * What it blocks by default, before the tool runs:
 *   1. Any path git would ignore in the repo it belongs to (`git check-ignore`).
 *   2. Any path whose name matches a common secret/credential shape, WHETHER
 *      OR NOT it is gitignored — because a secret that was never gitignored
 *      in the first place is exactly the case (1) cannot catch.
 *
 * Covers Read / Edit / Write / NotebookEdit (via tool_input.file_path) and
 * Glob / Grep (via tool_input.path) exactly — these carry a structured path,
 * so the match is reliable. Bash is covered on a best-effort basis only: the
 * command string is tokenized and each path-shaped token is checked the same
 * way. This is a heuristic, not a parser, and can be evaded by a sufficiently
 * indirect command. It is a backstop, not the reason this hook is safe to
 * rely on — the structured-path coverage above is.
 *
 * Override, deliberately inconvenient by design (see DATA-BOUNDARY.md):
 *   - Per path, durably: add the exact relative path to
 *     `.keel/data-boundary-allow` at the repo root, one path per line.
 *   - Per session, everything: set KEEL_DATA_BOUNDARY_OVERRIDE=1 in the
 *     environment the agent's tool calls actually run in. This is never set
 *     by anything in this factory — it has to be set by a human, on purpose,
 *     knowing what it turns off.
 *
 * Exit codes:
 *   0 = allow (no path found, path not sensitive, or explicitly allowlisted)
 *   2 = block (gitignored and/or secret-shaped path, no override present)
 */

'use strict';

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const MAX_STDIN = 1024 * 1024;

// Filenames that are secret-shaped but conventionally meant to be shared —
// checked before the denylist so a repo's own .env.example never trips this.
const SAFE_BASENAME_EXCEPTIONS = /(\.example|\.sample|\.template|\.dist)$/i;

// Matched against the basename first, then the full path, case-insensitively.
// Deliberately broad: a false positive costs one override; a false negative
// costs a credential in the model's context or a tool call's output.
const SECRET_PATTERNS = [
  /^\.env(\..+)?$/i,
  /secret/i,
  /credential/i,
  /(^|[._-])password([._-]|$)/i,
  /(^|[._-])passwd([._-]|$)/i,
  /(^|[._-])api[._-]?key/i,
  /\.pem$/i,
  /\.key$/i,
  /\.p12$/i,
  /\.pfx$/i,
  /\.jks$/i,
  /\.keystore$/i,
  /^id_(rsa|dsa|ecdsa|ed25519)$/i,
  /^\.npmrc$/i,
  /^\.pypirc$/i,
  /^\.netrc$/i,
  /^\.git-credentials$/i,
  /^credentials$/i, // e.g. .aws/credentials
  /^config$/i, // catches .aws/config and .kube/config alongside a path check below
  /kubeconfig/i,
  /\.tfstate(\.backup)?$/i,
  /service[._-]?account.*\.json$/i,
  /\.gpg$/i,
  /\.asc$/i,
  /wallet.*\.json$/i,
  /\.keychain(-db)?$/i,
];

// Path-fragment check for filenames too generic to denylist alone
// (`config`, `credentials`) — only sensitive inside one of these directories.
const SENSITIVE_DIR_FRAGMENTS = [
  /(^|\/)\.aws(\/|$)/i,
  /(^|\/)\.kube(\/|$)/i,
  /(^|\/)\.ssh(\/|$)/i,
  /(^|\/)\.gnupg(\/|$)/i,
  /(^|\/)\.config\/gcloud(\/|$)/i,
];

function isEnabled(value) {
  return ['1', 'true', 'yes', 'on'].includes(String(value || '').toLowerCase());
}

function basenameMatchesSecretPattern(basename) {
  if (SAFE_BASENAME_EXCEPTIONS.test(basename)) return null;
  for (const re of SECRET_PATTERNS) {
    if (re.test(basename)) return re.toString();
  }
  return null;
}

function pathMatchesSensitiveDir(relOrAbsPath) {
  const normalized = relOrAbsPath.replace(/\\/g, '/');
  for (const re of SENSITIVE_DIR_FRAGMENTS) {
    if (re.test(normalized)) return re.toString();
  }
  return null;
}

function findRepoRoot(startDir) {
  let dir = startDir;
  for (let i = 0; i < 64; i++) {
    if (fs.existsSync(path.join(dir, '.git'))) return dir;
    const parent = path.dirname(dir);
    if (parent === dir) return null;
    dir = parent;
  }
  return null;
}

function isGitIgnored(absPath) {
  const dir = path.dirname(absPath);
  if (!fs.existsSync(dir)) return false;
  const result = spawnSync('git', ['check-ignore', '-q', absPath], {
    cwd: dir,
    stdio: 'ignore',
  });
  // status 0 = ignored, 1 = not ignored, 128/null = not a repo or git missing
  return result.status === 0;
}

function isAllowlisted(absPath, repoRoot) {
  if (!repoRoot) return false;
  const allowFile = path.join(repoRoot, '.keel', 'data-boundary-allow');
  if (!fs.existsSync(allowFile)) return false;
  let lines;
  try {
    lines = fs.readFileSync(allowFile, 'utf8').split('\n');
  } catch {
    return false;
  }
  const relPath = path.relative(repoRoot, absPath).replace(/\\/g, '/');
  return lines
    .map(l => l.trim())
    .filter(l => l && !l.startsWith('#'))
    .some(l => l === relPath || l === absPath);
}

/**
 * Evaluate a single candidate path. Returns a block reason string, or null
 * if this path is fine.
 */
function evaluatePath(candidatePath, cwd) {
  if (!candidatePath) return null;
  const absPath = path.isAbsolute(candidatePath)
    ? candidatePath
    : path.resolve(cwd || process.cwd(), candidatePath);
  const basename = path.basename(absPath);

  const repoRoot = findRepoRoot(path.dirname(absPath));
  if (isAllowlisted(absPath, repoRoot)) return null;

  const secretMatch = basenameMatchesSecretPattern(basename);
  const dirMatch = pathMatchesSensitiveDir(absPath);
  const ignored = isGitIgnored(absPath);

  if (!secretMatch && !dirMatch && !ignored) return null;

  const reasons = [];
  if (ignored) reasons.push('matches this repo\'s .gitignore');
  if (secretMatch) reasons.push(`filename matches secret-shaped pattern ${secretMatch}`);
  if (dirMatch) reasons.push(`lives inside a sensitive directory (${dirMatch})`);

  return (
    `BLOCKED by data-boundary-guard: ${absPath}\n` +
    `Reason: ${reasons.join('; ')}.\n` +
    'This path was not touched. If this access is genuinely needed:\n' +
    `  - Durable, this path only: add "${repoRoot ? path.relative(repoRoot, absPath) : absPath}" ` +
    `to .keel/data-boundary-allow at the repo root.\n` +
    '  - This session only, everything: a human must set ' +
    'KEEL_DATA_BOUNDARY_OVERRIDE=1 in the environment — never do this yourself.\n' +
    'Do not retry via a different tool (cat, curl, a script) to route around this ' +
    'block. Stop and ask the user whether this specific access is intended.'
  );
}

// Very rough shell tokenizer: good enough to pull out path-shaped arguments
// for the best-effort Bash coverage. Not a substitute for the structured
// tool_input.file_path checks above.
function extractPathLikeTokens(command) {
  if (!command) return [];
  const tokens = command.split(/\s+/).filter(Boolean);
  return tokens
    .map(t => t.replace(/^['"]|['"]$/g, ''))
    .filter(t => t.includes('/') || /^\.[a-zA-Z]/.test(t) || SECRET_PATTERNS.some(re => re.test(t)))
    .filter(t => !t.startsWith('-') && !/^https?:\/\//i.test(t));
}

function parseInput(inputOrRaw) {
  if (typeof inputOrRaw === 'string') {
    try {
      return inputOrRaw.trim() ? JSON.parse(inputOrRaw) : {};
    } catch {
      return {};
    }
  }
  return inputOrRaw && typeof inputOrRaw === 'object' ? inputOrRaw : {};
}

/**
 * Exportable run() for in-process execution via run-with-flags.js.
 */
function run(inputOrRaw) {
  if (isEnabled(process.env.KEEL_DATA_BOUNDARY_OVERRIDE)) {
    return { exitCode: 0 };
  }

  const input = parseInput(inputOrRaw);
  const toolInput = input?.tool_input || {};
  const cwd = input?.cwd || process.cwd();

  const candidates = [];
  if (typeof toolInput.file_path === 'string') candidates.push(toolInput.file_path);
  if (typeof toolInput.file === 'string') candidates.push(toolInput.file);
  if (typeof toolInput.path === 'string') candidates.push(toolInput.path);
  if (typeof toolInput.notebook_path === 'string') candidates.push(toolInput.notebook_path);
  if (typeof toolInput.command === 'string') {
    candidates.push(...extractPathLikeTokens(toolInput.command));
  }

  for (const candidate of candidates) {
    const reason = evaluatePath(candidate, cwd);
    if (reason) {
      return { exitCode: 2, stderr: reason };
    }
  }

  return { exitCode: 0 };
}

module.exports = { run };

// Stdin fallback for spawnSync execution — only when invoked directly.
if (require.main === module) {
  let raw = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', chunk => {
    if (raw.length < MAX_STDIN) {
      raw += chunk.substring(0, MAX_STDIN - raw.length);
    }
  });

  process.stdin.on('end', () => {
    const result = run(raw);

    if (result.stderr) {
      process.stderr.write(result.stderr + '\n');
    }

    if (result.exitCode === 2) {
      process.exit(2);
    }

    process.stdout.write(raw);
  });
}
