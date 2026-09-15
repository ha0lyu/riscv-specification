#!/bin/sh
set -eu

skill_dir="${HOME}/.codex/skills/riscv-spec"
PARENT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

mkdir -p "${skill_dir}/agents"
cp "$PARENT_DIR/riscv-spec-skill/SKILL.md" "${skill_dir}/SKILL.md"
cp "$PARENT_DIR/riscv-spec-skill/agents/openai.yaml" "${skill_dir}/agents/openai.yaml"
printf 'Installed RISC-V skill at %s\n' "${skill_dir}"

echo 'export SPEC_SKILL_ROOT="'"$PARENT_DIR"'"' >> ~/.profile
