---
title: "WooCommerce API Sanitizer"
description: "WordPress plugin that normalises spaces in WooCommerce product variant attributes received via the REST API, fixing variation matching failures."
github: "https://github.com/edleeman17/WooCommerce-API-Sanitizer"
language: "PHP"
stars: 0
status: "active"
---

WooCommerce has a longstanding issue where non-breaking spaces or multiple spaces in attribute values sent via the REST API cause variation matching to fail silently — the variation defaults to "Any [attribute]" instead of matching the existing term.

This plugin hooks into the API request pipeline and normalises whitespace before WooCommerce processes it. Small fix, annoying problem.

**Tech:** PHP, WordPress, WooCommerce REST API
