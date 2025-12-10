# Home Assistant Configuration

Personal Home Assistant configuration with a modular YAML structure and [UI Lovelace Minimalist](https://ui-lovelace-minimalist.github.io/UI/) dashboard.

## Structure

```
configuration.yaml          # Main entry point
├── automations.yaml        # Automation rules
├── scripts.yaml            # Reusable scripts
├── scenes.yaml             # Scene definitions
├── groups.yaml             # Entity groups
├── includes/               # Modular configs by domain
│   ├── sensors.yaml
│   ├── lights.yaml
│   ├── climate.yaml
│   ├── switches.yaml
│   ├── templates/          # Template sensors
│   └── ...
└── ui_lovelace_minimalist/ # Custom dashboard
    ├── custom_cards/
    └── dashboard/
```

## Dashboard Screenshots

<img src="https://github.com/mekenthompson/ui-lovelace-minimalist-config/blob/ba0eccd18d52c267219c6648a296f6832efd920b/mekenthompson-minimalist-1-home.png" width="250">
<img src="https://github.com/mekenthompson/ui-lovelace-minimalist-config/blob/ba0eccd18d52c267219c6648a296f6832efd920b/mekenthompson-minimalist-2-lights.png" width="250">
<img src="https://github.com/mekenthompson/ui-lovelace-minimalist-config/blob/ba0eccd18d52c267219c6648a296f6832efd920b/mekenthompson-minimalist-3-heating.png" width="250">
<img src="https://github.com/mekenthompson/ui-lovelace-minimalist-config/blob/ba0eccd18d52c267219c6648a296f6832efd920b/mekenthompson-minimalist-4-cooling.png" width="250">
<img src="https://github.com/mekenthompson/ui-lovelace-minimalist-config/blob/ba0eccd18d52c267219c6648a296f6832efd920b/mekenthompson-minimalist-5-audio.png" width="250">
<img src="https://github.com/mekenthompson/ui-lovelace-minimalist-config/blob/ba0eccd18d52c267219c6648a296f6832efd920b/mekenthompson-minimalist-6-tv.png" width="250">
