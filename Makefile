HUGO_IMG := klakegg/hugo:ext-alpine

.PHONY: build serve

build:
	docker run --rm -v "$(PWD)":/src $(HUGO_IMG)
	npx --yes pagefind --site public

serve:
	docker run --rm -v "$(PWD)":/src -p 1313:1313 $(HUGO_IMG) server --bind 0.0.0.0
