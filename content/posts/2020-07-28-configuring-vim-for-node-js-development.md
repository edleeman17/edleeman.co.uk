---
title: Configuring Vim for Node Js Development
slug: configuring-vim-for-node-js-development
date: 2020-07-28T18:58:00.000Z
type: post
---



## Using Vim

If you have come across this article, I probably don't need to explain why you need to use Vim as your development IDE.

You're probably here because you want to use Vim, but not sure how to integrate it into your current workflow.

I was in the same position a few months ago.

The easiest way is to install a vim extension into your current IDE of choice, this will bring all of the features of vim into your current workflow.

After getting used to Vim, in something that you're familiar with. You'll probably want to jump-ship into full-blown Vim.

That's what this blog post is for.

### The Primeagen

A lot of my configuration and interest in jumping over to Vim came from [The Primeagen](https://www.youtube.com/channel/UC8ENHE5xdFSwx71u3fDH5Xw).

This guy is a machine with Vim.

He's currently a Netflix Engineer who only works in Vim for his day-to-day work. Regularly streaming over on [Twitch](https://www.twitch.tv/theprimeagen) and uploading on [YouTube](https://www.youtube.com/channel/UC8ENHE5xdFSwx71u3fDH5Xw).

He has recently produced a series on [Vim As Your Editor](https://www.youtube.com/playlist?list=PLm323Lc7iSW_wuxqmKx_xxNtJC_hJbQ7R). I highly recommend that you go and watch it.

## Plugins

Vim is highly configurable with user-created plugins.

Here's a list that I recommend to use with Node.Js:

- [vim-fugitive](https://github.com/tpope/vim-fugitive)
- This integrates Git seemlessly into Vim

- [coc.nvim](https://github.com/neoclide/coc.nvim)
- This allows code completion and intellisense for Javascript in Vim

- [nerdcommenter](https://github.com/preservim/nerdcommenter)
- A simple plugin to comment out lines of code using Vim bindings

- [ale](https://github.com/dense-analysis/ale)
- A syntax highlighter for Vim

- [nerdtree](https://github.com/preservim/nerdtree)
- A file tree view for selecting files and navigating folder structure in your projects

- [lightline](https://github.com/itchyny/lightline.vim)
- A lightweight status bar to show progress in your buffer and other useful information

- [fzf](https://github.com/junegunn/fzf.vim)
- A file-finding plugin to quickly search your project and swtich buffers

- [gruvbox](https://github.com/morhetz/gruvbox)
- The only theme you should be using. Heavily influenced by The Primeagen

- [vim-buftabline](https://github.com/ap/vim-buftabline)
- Introduces 'tabs' into Vim for keeping track of your open buffers

Installing plugins is easy in Vim. I use a plugin manager called [vim-plug](https://github.com/junegunn/vim-plug).

## .vimrc.plug

Your plugin installation lives in a file called `.vimrc.plug`.

Here's a copy of my `.vimrc.plug` as an example

    " .vimrc.plug
    
    call plug#begin('~/.vim/plugged')
    " Git
    Plug 'tpope/vim-fugitive'
    
    " Code completion
    Plug 'neoclide/coc.nvim', {'branch': 'release'}
    
    " Code commenter
    Plug 'preservim/nerdcommenter'
    "
    " Syntax highlighting
    Plug 'dense-analysis/ale'
    
    " NERDTree
    Plug 'preservim/nerdtree'
    "
    " Statusbar
    Plug 'itchyny/lightline.vim'
    "
    " Finder
    Plug 'junegunn/fzf', { 'do': { -> fzf#install() } }
    Plug 'junegunn/fzf.vim'
    
    " File finder
    Plug 'vifm/vifm.vim'
    
    " Theme
    Plug 'morhetz/gruvbox'
    
    " Tabs
    Plug 'ap/vim-buftabline'
    
    call plug#end()
    
    set background=dark
    colorscheme gruvbox
    

Just install those plugins using `:PlugInstall`

## .vimrc

`.vimrc` is your main Vim config file. You probably know this already.

Here's mine:

    syntax on
    
    set guicursor=
    set noshowmatch
    set relativenumber
    set nohlsearch
    set hidden
    set noerrorbells
    set tabstop=4 softtabstop=4
    set shiftwidth=4
    set expandtab
    set smartindent
    set nu
    set nowrap
    set smartcase
    set noswapfile
    set nobackup
    set undodir=~/.vim/undodir
    set undofile
    set incsearch
    set termguicolors
    set scrolloff=8
    set modifiable
    
    " Give more space for displaying messages.
    set cmdheight=2
    
    " Having longer updatetime (default is 4000 ms = 4 s) leads to noticeable
    " delays and poor user experience.
    set updatetime=50
    
    " Don't pass messages to |ins-completion-menu|.
    set shortmess+=c
    
    set colorcolumn=100
    highlight ColorColumn ctermbg=0 guibg=lightgrey
    
    map <C-n> :NERDTreeToggle<CR>
    map <C-p> :Files<CR>
    map <C-f> :Rg<CR>
    map <C-t> :e <cfile><cr>
    map <S-Tab> :bn<CR>
    map <F5> :setlocal spell! spelllang=en_gb<CR>
    
    let loaded_matchparen = 1
    let mapleader = " "
    
    " CoC
    " GoTo code navigation.
    nmap <leader>gd <Plug>(coc-definition)
    nmap <leader>gy <Plug>(coc-type-definition)
    nmap <leader>gi <Plug>(coc-implementation)
    nmap <leader>gr <Plug>(coc-references)
    nmap <leader>rr <Plug>(coc-rename)
    nmap <leader>g[ <Plug>(coc-diagnostic-prev)
    nmap <leader>g] <Plug>(coc-diagnostic-next)
    nmap <silent> <leader>gp <Plug>(coc-diagnostic-prev-error)
    nmap <silent> <leader>gn <Plug>(coc-diagnostic-next-error)
    nnoremap <leader>cr :CocRestart
    
    " Sweet Sweet FuGITive
    nmap <leader>gj :diffget //3<CR>
    nmap <leader>gf :diffget //2<CR>
    nmap <leader>gs :G<CR>
    
    " Search and replace hotkey
    nnoremap H :%s//gc<left><left><left>
    
    " Move highlighted text up and down
    vnoremap J :m '>+1<CR>gv=gv
    vnoremap K :m '<-2<CR>gv=gv
    
    " Import plugins
    if filereadable(expand("~/.vimrc.plug"))
        source ~/.vimrc.plug
    endif
    
    " Status bar config
    set statusline+=%#warningmsg#
    
    " Fix files automatically on save
    let g:ale_fixers = {}
    let g:ale_javascript_eslint_use_global = 1
    let g:ale_linters = {
      \'javascript': ['eslint'],
      \'vue': ['eslint', 'stylelint', 'tsserver'],
    \}
    
    let g:ale_fixers = {
      \'javascript': ['prettier', 'eslint'],
      \'vue': ['eslint', 'stylelint'],
    \}
    
    let g:ale_linters_explicit = 1
    let g:ale_sign_column_always = 1
    let g:ale_sign_error = '>>'
    let g:ale_sign_warning = '--'
    let g:ale_fix_on_save = 1
    
    " Close NERDTree when closing the last buffer
    autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
    
    fun! TrimWhitespace()
        let l:save = winsaveview()
        keeppatterns %s/\s\+$//e
        call winrestview(l:save)
    endfun
    
    autocmd BufWritePre * :call TrimWhitespace()
    
    command! -bang -nargs=* Rg
      \ call fzf#vim#grep(
      \   'rg --column --line-number --no-heading --color=always --smart-case -- '.shellescape(<q-args>), 1,
      \   fzf#vim#with_preview(), <bang>0)
    
    

There is some initial setup prior to using this configuration. Such as:

- Running `:CocInstall coc-tsserver`
- Installing fzf `sudo apt-get install fzf`
- Installing Rg `sudo apt-get install ripgrep`

## Final points

Vim is a steep learning curve. Get used to Vim by using a plugin in your existing IDE, once comfortable, switch to Vim.

Let me know if this post has helped you in the comments below, I'd appreciate your feedback.
