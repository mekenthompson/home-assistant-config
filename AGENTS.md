# Home Assistant Configuration

## Validation Commands
```bash
hass --script check_config -c .    # Validate configuration (run in HA container)
yamllint .                          # Lint YAML files
```

## Architecture
- `configuration.yaml` - Main entry point, imports all other configs via `!include`
- `includes/` - Modular configs: sensors, lights, switches, climate, fans, etc.
- `includes/templates/` - Template sensors (merged via `!include_dir_merge_list`)
- `ui_lovelace_minimalist/` - Custom dashboard cards and views
- `automations.yaml`, `scripts.yaml`, `scenes.yaml` - Root-level HA primitives

## Code Style
- Use 2-space indentation for YAML
- Group related entities in their respective include files
- Use `!include` for modularity; `!include_dir_merge_list` for template dirs
- Entity naming: `domain.descriptive_snake_case` (e.g., `sensor.living_room_temp`)
- Use meaningful automation IDs and aliases
- Comment out unused integrations rather than deleting (for reference)

## Secrets
- All credentials use `!secret` references (stored in `secrets.yaml`, gitignored)
- Never hardcode passwords, tokens, or API keys in committed files
- `secrets.yaml`, `known_devices.yaml`, and `ip_bans.yaml` are gitignored
