---
title: "Fixing Syntax Highlighting for Hugo Chroma iOS"
date: 2024-02-12T23:42:41Z
draft: false
type: "note"
---

# Fixing Syntax highlighting for Hugo chroma in iOS

I recently came across the issue of text being different sizes when displayed as a code fence in Hugo.

![Invalid Chroma formatting in iOS](/images/invalid-formatting-in-ios.png)

It was hard to debug as at only seemed to happen on iOS in both Chrome and Safari. It wasn't happening on the desktop so I wasn't able to jump into dev tools to inspect why the elements are displaying as different sizes.

It turns out that it's an issue with how iOS inteprets Flexbox.

I needed to add the following CSS to combat this issue.

```css
code {
    /* Fixes iOS font sizing anomaly */
    text-size-adjust: 100%;
    -ms-text-size-adjust: 100%;
    -moz-text-size-adjust: 100%;
    -webkit-text-size-adjust: 100%;
}
```

I found the solution [here](https://github.com/adityatelange/hugo-PaperMod/issues/828)
