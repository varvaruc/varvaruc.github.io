"Forget compatibility with Vi. Who cares.
set nocompatible

"for vundle
filetype off 

"Write the old file out when switching between files.
set autowrite

"Display current cursor position in lower right corner.
set ruler

"enable syntax
syntax on

"Tab stuff
set softtabstop=4 "go back one tab when hitting backspace(without this is goes back single space)
set tabstop=4 "used by >>, << and tab.
set shiftwidth=4 "number of space characters used when displaying TAB
set expandtab "replace tab by spaces

"Indent stuff
set smartindent
set autoindent

"working backspace
set backspace=indent,eol,start
fixdel

"case insensitive search
set ignorecase
set smartcase

"highlight search
set hlsearch

"incremental search
set incsearch

"better line wrappings
set wrap
set textwidth=79
set formatoptions=qrn1

"disable menus in GUI
set guioptions-=m
set guioptions-=T

"show line numbers
set number
set laststatus=2
set cursorline
set t_Co=256 "xterm 256 colors
set encoding=utf-8

" Key mappings
" Move visual blocks up and down with <C-j> and <C-k>
nnoremap <C-j> :m .+1<CR>==
nnoremap <C-k> :m .-2<CR>==
inoremap <C-j> <Esc>:m .+1<CR>==gi
inoremap <C-k> <Esc>:m .-2<CR>==gi
vnoremap <C-j> :m '>+1<CR>gv=gv
vnoremap <C-k> :m '<-2<CR>gv=gv

"disable arrow keys in normal mode
map <up> <nop>
map <down> <nop>
map <left> <nop>
map <right> <nop>

"disable arrow keys in insert mode
imap <up> <nop>
imap <down> <nop>
imap <left> <nop>
imap <right> <nop>

"Redraws screen no highlighting
nnoremap <silent> <C-l> :nohl<CR><C-l>

"Better wrap navigation
nnoremap j gj
nnoremap k gk
nnoremap gj j
nnoremap gk k

"ESC with jj
imap jj <Esc>

"Complete brackets
inoremap {      {}<Left>
inoremap {<CR>  {<CR>}<Esc>O
inoremap {{     {
inoremap {}     {}

"Uppercase type proof
:command! WQ wq
:command! W w
:command! Wq wq
:command! Q q

"Print colon when hitting semicolor
map ; :

"Leader is now a comma 
let mapleader = ","

":grep 'word' %:p:h\*
"results forward
nmap <Leader>rf :cn<CR>zv

" results backwards
nmap <Leader>rb :cp<CR>zv
nmap <tab> <c-w><c-w>

"Bubble single lines (kicks butt)
"http://vimcasts.org/episodes/bubbling-text/
nmap <C-Up> ddkP
nmap <C-Down> ddp

"Bubble multiple lines
vmap <C-Up> xkP`[V`]
vmap <C-Down> xp`[V`]


filetype plugin indent on

"colorscheme
"colorscheme twilight
set guifont=Consolas:h12:cANSI

"enable scrolling
set mouse=a

"open current buffer in chrome/firefox
abbrev gc :!chrome %<cr>
abbrev ff :!firefox %<cr>

"insert current time (for temp files).
cmap <F3> <C-R>=strftime("_%d_%m_%Y_%H_%M")<CR>

"hex view ( works on linux )
map <Leader>hx :%!xxd<cr>
map <Leader>hxr :%!xxd -r<cr>

"remove default binding for CtrlP, interacts with emmet-vim ctrl-p
let g:ctrlp_map = ''

"enable folding
set foldmethod=indent

"open files unfolded
set foldlevel=99


"Ever notice a slight lag after typing the leader key + command? This lowers
"the timeout.
set timeoutlen=500

"Switch between buffers without saving
set hidden
 
"Show command in bottom right portion of the screen
set showcmd

"Split windows below the current window.
set splitbelow              

" enable vertical ruler
"set cursorline cursorcolumn
