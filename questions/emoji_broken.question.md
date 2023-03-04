---
title: "Why does emoji break alignment in a Table or Panel?"
---

Certain emoji take up double space within the terminal. Unfortunately, terminals don't always agree how wide a given character should be.

Rich has no way of knowing how wide a character will be on any given terminal. This can break alignment in containers like Table and Panel, where Rich needs to know the width of the content.

There are also *multiple codepoints* characters, such as country flags, and emoji modifiers, which produce wildly different results across terminal emulators. 

Fortunately, most characters will work just fine. But you may have to avoid using the emojis that break alignment. You will get good results if you stick to emoji released on or before version 9 of the Unicode database, 
