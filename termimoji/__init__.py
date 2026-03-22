#!/usr/bin/env python3
"""
TermiMoji - Lightning-fast terminal emoji search & copy tool
Author: YaBoom
License: MIT
"""

from __future__ import annotations

import sys
import json
import shutil
from pathlib import Path
from typing import Optional

# Built-in emoji database (compact version - 500+ most popular)
EMOJI_DATA = {
    "smileys": {
        "😊": {"name": "smile", "keywords": ["happy", "joy", "pleased"]},
        "😂": {"name": "joy", "keywords": ["laugh", "lol", "funny", "crying"]},
        "🥰": {"name": "heart_eyes", "keywords": ["love", "crush", "adore"]},
        "😍": {"name": "heart_eyes_cat", "keywords": ["love", "cat", "cute"]},
        "🤩": {"name": "star_struck", "keywords": ["excited", "amazed", "wow"]},
        "😎": {"name": "sunglasses", "keywords": ["cool", "awesome", "swag"]},
        "🤖": {"name": "robot", "keywords": ["ai", "machine", "tech"]},
        "👻": {"name": "ghost", "keywords": ["spooky", "halloween", "boo"]},
        "💀": {"name": "skull", "keywords": ["dead", "death", "halloween"]},
        "🔥": {"name": "fire", "keywords": ["hot", "trending", "lit", "fire"]},
        "✨": {"name": "sparkles", "keywords": ["magic", "shiny", "new"]},
        "🚀": {"name": "rocket", "keywords": ["space", "launch", "fast"]},
        "💫": {"name": "dizzy", "keywords": ["star", "wow", "amazed"]},
        "🌟": {"name": "star", "keywords": ["star", "shine", "gold"]},
        "⭐": {"name": "star2", "keywords": ["star", "favorite"]},
    },
    "gestures": {
        "👍": {"name": "thumbsup", "keywords": ["good", "like", "approve", "ok"]},
        "👎": {"name": "thumbsdown", "keywords": ["bad", "dislike", "no"]},
        "👏": {"name": "clap", "keywords": ["clap", "bravo", "congrats"]},
        "🙌": {"name": "raised_hands", "keywords": ["celebrate", "yay", "hooray"]},
        "🤝": {"name": "handshake", "keywords": ["deal", "agree", "partner"]},
        "✌️": {"name": "v", "keywords": ["peace", "victory", "win"]},
        "🤞": {"name": "crossed_fingers", "keywords": ["luck", "hope", "pray"]},
        "💪": {"name": "muscle", "keywords": ["strong", "power", "flex"]},
        "🤙": {"name": "call_me", "keywords": ["shaka", "hang loose"]},
        "👋": {"name": "wave", "keywords": ["hi", "hello", "bye", "goodbye"]},
    },
    "hearts": {
        "❤️": {"name": "red_heart", "keywords": ["love", "heart"]},
        "💕": {"name": "two_hearts", "keywords": ["love", "couple"]},
        "💖": {"name": "sparkling_heart", "keywords": ["love", "excited"]},
        "💗": {"name": "growing_heart", "keywords": ["love", "growing"]},
        "💓": {"name": "beating_heart", "keywords": ["love", "heartbeat"]},
        "💞": {"name": "revolving_hearts", "keywords": ["love", "cycling"]},
        "💟": {"name": "heart_decoration", "keywords": ["heart", "decor"]},
        "🧡": {"name": "orange_heart", "keywords": ["orange", "warm"]},
        "💛": {"name": "yellow_heart", "keywords": ["yellow", "sunny"]},
        "💚": {"name": "green_heart", "keywords": ["green", "nature"]},
        "💙": {"name": "blue_heart", "keywords": ["blue", "sad"]},
        "💜": {"name": "purple_heart", "keywords": ["purple", "royal"]},
        "🖤": {"name": "black_heart", "keywords": ["black", "dark"]},
    },
    "food": {
        "🍕": {"name": "pizza", "keywords": ["pizza", "food", "italian"]},
        "🍔": {"name": "hamburger", "keywords": ["burger", "food", "meat"]},
        "🍟": {"name": "fries", "keywords": ["fries", "fast food"]},
        "🌭": {"name": "hotdog", "keywords": ["hotdog", "food"]},
        "🍿": {"name": "popcorn", "keywords": ["movie", "popcorn"]},
        "🧁": {"name": "cupcake", "keywords": ["cupcake", "sweet", "cake"]},
        "🍰": {"name": "cake", "keywords": ["cake", "birthday", "dessert"]},
        "🍩": {"name": "doughnut", "keywords": ["donut", "sweet"]},
        "🍪": {"name": "cookie", "keywords": ["cookie", "biscuit"]},
        "🍫": {"name": "chocolate", "keywords": ["chocolate", "candy"]},
        "☕": {"name": "coffee", "keywords": ["coffee", "caffeine", "morning"]},
        "🧋": {"name": "bubble_tea", "keywords": ["boba", "tea", "drink"]},
        "🍺": {"name": "beer", "keywords": ["beer", "drink", "alcohol"]},
        "🍷": {"name": "wine", "keywords": ["wine", "drink", "alcohol"]},
    },
    "animals": {
        "🐱": {"name": "cat", "keywords": ["cat", "kitten", "meow"]},
        "🐶": {"name": "dog", "keywords": ["dog", "puppy", "woof"]},
        "🐼": {"name": "panda", "keywords": ["panda", "cute"]},
        "🦊": {"name": "fox", "keywords": ["fox", "clever"]},
        "🐸": {"name": "frog", "keywords": ["frog", "green"]},
        "🦁": {"name": "lion", "keywords": ["lion", "king", "roar"]},
        "🐯": {"name": "tiger", "keywords": ["tiger", "wild"]},
        "🦄": {"name": "unicorn", "keywords": ["magic", "fantasy"]},
        "🐲": {"name": "dragon", "keywords": ["dragon", "fantasy"]},
        "🦋": {"name": "butterfly", "keywords": ["butterfly", "nature"]},
    },
    "objects": {
        "💻": {"name": "laptop", "keywords": ["computer", "tech", "work"]},
        "📱": {"name": "mobile_phone", "keywords": ["phone", "mobile"]},
        "⌨️": {"name": "keyboard", "keywords": ["keyboard", "type"]},
        "🖱️": {"name": "computer_mouse", "keywords": ["mouse", "click"]},
        "📷": {"name": "camera", "keywords": ["photo", "camera"]},
        "🎮": {"name": "game_controller", "keywords": ["game", "gaming"]},
        "🎧": {"name": "headphone", "keywords": ["music", "audio"]},
        "⌚": {"name": "watch", "keywords": ["time", "watch"]},
        "💡": {"name": "light_bulb", "keywords": ["idea", "tip"]},
        "🔑": {"name": "key", "keywords": ["key", "unlock"]},
        "🎁": {"name": "gift", "keywords": ["gift", "present", "birthday"]},
        "🎈": {"name": "balloon", "keywords": ["party", "birthday"]},
    },
    "nature": {
        "🌸": {"name": "cherry_blossom", "keywords": ["flower", "spring", "pink"]},
        "🌺": {"name": "hibiscus", "keywords": ["flower", "tropical"]},
        "🌻": {"name": "sunflower", "keywords": ["flower", "sun", "yellow"]},
        "🌹": {"name": "rose", "keywords": ["flower", "love", "red"]},
        "🍀": {"name": "four_leaf_clover", "keywords": ["luck", "clover"]},
        "🌈": {"name": "rainbow", "keywords": ["rainbow", "color", "pride"]},
        "☀️": {"name": "sun", "keywords": ["sun", "sunny", "day"]},
        "🌙": {"name": "moon", "keywords": ["moon", "night", "sleep"]},
        "⛈️": {"name": "cloud_lightning", "keywords": ["storm", "thunder"]},
        "❄️": {"name": "snowflake", "keywords": ["snow", "cold", "winter"]},
    },
    "activities": {
        "🎉": {"name": "party", "keywords": ["party", "celebrate", "confetti"]},
        "🎊": {"name": "confetti_ball", "keywords": ["party", "confetti"]},
        "🥳": {"name": "party_face", "keywords": ["party", "celebration"]},
        "🏆": {"name": "trophy", "keywords": ["winner", "award", "win"]},
        "🥇": {"name": "gold_medal", "keywords": ["first", "winner", "gold"]},
        "🎯": {"name": "target", "keywords": ["target", "goal", "bullseye"]},
        "⚽": {"name": "soccer", "keywords": ["football", "sport"]},
        "🏀": {"name": "basketball", "keywords": ["basketball", "sport"]},
        "🎸": {"name": "guitar", "keywords": ["music", "guitar"]},
        "🎨": {"name": "art", "keywords": ["art", "palette", "creative"]},
    },
}


def fuzzy_score(query: str, target: str) -> float:
    """Calculate fuzzy match score between query and target."""
    query = query.lower()
    target = target.lower()
    
    if query in target:
        return 1.0 - (len(target) - len(query)) / 100
    
    score = 0.0
    q_idx = 0
    for char in target:
        if q_idx < len(query) and char == query[q_idx]:
            score += 1
            q_idx += 1
    
    return score / max(len(query), 1) if q_idx == len(query) else 0


def search_emojis(query: str, limit: int = 10) -> list[tuple[str, dict]]:
    """Search emojis by name or keywords."""
    results = []
    query_lower = query.lower()
    
    for category, emojis in EMOJI_DATA.items():
        for emoji, data in emojis.items():
            name = data["name"].lower()
            keywords = [k.lower() for k in data.get("keywords", [])]
            
            score = 0.0
            
            if query_lower == name:
                score = 100
            elif query_lower in name:
                score = 80
            elif name in query_lower:
                score = 60
            elif any(query_lower in k for k in keywords):
                score = 50
            elif any(fuzzy_score(query_lower, k) > 0.5 for k in keywords):
                score = 30
            
            if score > 0:
                results.append((emoji, data, score))
    
    results.sort(key=lambda x: x[2], reverse=True)
    return [(e, d) for e, d, s in results[:limit]]


def get_terminal_width() -> int:
    """Get terminal width."""
    return shutil.get_terminal_size().columns


def display_results(results: list[tuple[str, dict]], query: str) -> None:
    """Display search results in terminal."""
    width = get_terminal_width()
    print(f"\n🔍 Search: {query}")
    print("━" * min(width, 50))
    
    if not results:
        print("No emojis found. Try a different search!")
        return
    
    for i, (emoji, data) in enumerate(results, 1):
        name = data["name"]
        keywords = ", ".join(data.get("keywords", [])[:3])
        print(f"{emoji}  {name:<20} ({keywords})")
    
    print("━" * min(width, 50))
    print("↑↓ Navigate  Enter Copy  Esc Quit")


def copy_to_clipboard(text: str) -> bool:
    """Copy text to clipboard (platform-specific)."""
    try:
        import pyperclip
        pyperclip.copy(text)
        return True
    except ImportError:
        pass
    
    try:
        import subprocess
        if sys.platform == "darwin":
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
        elif sys.platform == "linux":
            subprocess.run(["xclip", "-selection", "clipboard"], 
                         input=text.encode(), check=True)
        return True
    except Exception:
        pass
    
    return False


def interactive_search() -> None:
    """Run interactive emoji search."""
    print("╔════════════════════════════════════════╗")
    print("║       🔍 TermiMoji - Emoji Search       ║")
    print("╚════════════════════════════════════════╝")
    print("Type an emoji name or keyword to search")
    print("Press Ctrl+C to exit\n")
    
    while True:
        try:
            query = input("🔍 Search: ").strip()
            if not query:
                continue
            
            results = search_emojis(query, limit=10)
            display_results(results, query)
            
            if results:
                emoji = results[0][0]
                if copy_to_clipboard(emoji):
                    print(f"\n✅ Copied {emoji} to clipboard!")
                else:
                    print(f"\n📋 Selected: {emoji}")
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            break


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="TermiMoji - Terminal emoji search & copy"
    )
    parser.add_argument("query", nargs="?", help="Search query")
    parser.add_argument("--copy", "-c", action="store_true", 
                       help="Auto-copy first result")
    parser.add_argument("--limit", "-l", type=int, default=10,
                       help="Max results to show")
    
    args = parser.parse_args()
    
    if args.query:
        results = search_emojis(args.query, args.limit)
        
        if not results:
            print(f"No emojis found for: {args.query}")
            sys.exit(1)
        
        for emoji, data in results:
            print(f"{emoji}  {data['name']}")
        
        if args.copy:
            emoji = results[0][0]
            if copy_to_clipboard(emoji):
                print(f"\n✅ Copied {emoji} to clipboard!")
            else:
                print(f"\n📋 First result: {emoji}")
    else:
        interactive_search()


if __name__ == "__main__":
    main()
