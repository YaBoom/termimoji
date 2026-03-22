# 🔍 TermiMoji

<p align="center">
  <img src="https://img.shields.io/pypi/v/termimoji?style=flat&color=FF69B4" alt="PyPI">
  <img src="https://img.shields.io/pypi/pyversions/termimoji" alt="Python">
  <img src="https://img.shields.io/github/license/YaBoom/termimoji" alt="License">
</p>

> A lightning-fast terminal emoji search & copy tool with fuzzy matching. Never struggle finding the perfect emoji again! ✨

## ✨ Features

- 🚀 **Lightning Fast** - Instant fuzzy search across 3000+ emojis
- 🎯 **Smart Fuzzy Matching** - Find emojis even with typos
- 📋 **One-Click Copy** - Auto-copy to clipboard with zero friction
- 🎨 **Rich Categories** - Search by keywords, emotions, or activities
- 🌙 **Dark Mode** - Beautiful default theme for terminal
- ⚡ **Zero Dependencies** - Pure Python, no bloat

## 📦 Installation

```bash
# Via pip (from PyPI, if published)
pip install termimoji

# Via uv (faster, from PyPI, if published)
uv add termimoji

# For local development
pip install .
# or
uv pip install .
```

## 🎮 Usage

```bash
# Interactive search mode
termimoji

# Quick search from command line
termimoji "party"
termimoji "fire" --copy
termimoji "cat" --limit 5
```

### Interactive Mode

```
🔍 Search: love
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
❤️  red_heart     love      hearts    love_letter
💕  two_hearts    sparkling_heart  heart_eyes
💖  growing_heart  heart_with_arrow
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
↑↓ Navigate  Enter Copy  Esc Quit
```

## 🧩 Example Searches

| Query | Results |
|-------|---------|
| `party` | 🎉 🎊 🥳 🎈 |
| `fire` | 🔥 🚒 🧨 💥 |
| `cat` | 🐱 😺 😸 😹 |
| `coffee` | ☕ 🫖 🥤 🍵 |
| `money` | 💰 💵 💴 💶 |

## 🛠️ Configuration

Create `~/.termimoji/config.json`:

```json
{
  "limit": 10,
  "auto_copy": true,
  "theme": "dark",
  "categories": ["smileys", "animals", "food"]
}
```

## 📋 Requirements

- Python 3.10+
- pip / uv

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit PRs

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

<p align="center">Made with ❤️ for terminal lovers</p>
