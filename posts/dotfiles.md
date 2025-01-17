Dotfiles
2-12-2015


**[TL;DR](http://en.wikipedia.org/wiki/Wikipedia:Too_long;_didn't_read)** -- Dotfiler er (næsten) uundværlige i opsætningen af Mac - eller Linux - hvis man vil lidt ud over hvad der lige rummes i Systemindstillinger. Det her er mine dotfiler.

![MacBook Pro](/static/20151202_macbook-pro.jpg)

### Om dotfiler generelt

Hvis man en gang i mellem reinstallerer sin computer eller har flere maskiner, som man veksler i mellem og godt kan lide at den opfører sig på (nogenlunde) samme måde uanset hvilken man sidder ved eller om man lige har reinstalleret, så er dotfiles smarte.

Kort beskrevet, så er dotfiles en måde at beskrive hvordan en computer skal sættes op på i et meget robust format[^1].

Filerne bliver læst på forskellige tidspunkter alt efter hvilken fil der er tale om, og jeg har endnu ikke fundet en bedre beskrivelse af det end denne på "[The Lumber Room](https://shreevatsa.wordpress.com/2008/03/30/zshbash-startup-files-loading-order-bashrc-zshrc-etc/)"[^2].

Problemet med at beskrive hvornår hvad læses er, at Bash trækker på forskellige filer alt efter hvilken slags shell den mener den kører i. Eks.: for en "interaktiv ikke-login-shell", læses .bashrc, men for en "interaktiv login-shell" læser den udelukkende fra den første af .bash_profile, .bash_login og .profile. Der er ingen fornuftig grund til, at det er sådan, sådan er det bare...

Bash læser dotfilerne således (læs nedad i den relevante kolonne. Først udføres A, så B, så C osv. B1, B2, B3 betyder at bash kun udfører den første af disse filer, den støder på):

	+----------------+-----------+-----------+-------+
	|                |Interactive|Interactive|Script*|
	|                |login      |non-login  |       |
	+----------------+-----------+-----------+-------+
	|/etc/profile    |   A       |           |       |
	+----------------+-----------+-----------+-------+
	|/etc/bash.bashrc|           |    A      |       |
	+----------------+-----------+-----------+-------+
	|~/.bashrc       |           |    B      |       |
	+----------------+-----------+-----------+-------+
	|~/.bash_profile |   B1      |           |       |
	+----------------+-----------+-----------+-------+
	|~/.bash_login   |   B2      |           |       |
	+----------------+-----------+-----------+-------+
	|~/.profile      |   B3      |           |       |
	+----------------+-----------+-----------+-------+
	|BASH_ENV        |           |           |  A    |
	+----------------+-----------+-----------+-------+
	|                |           |           |       |
	+----------------+-----------+-----------+-------+
	|                |           |           |       |
	+----------------+-----------+-----------+-------+
	|~/.bash_logout  |    C      |           |       |
	+----------------+-----------+-----------+-------+

	* Or non-interactive non-login.

På en Mac afvikles en ny terminal et interaktivt login; på en linux-boks som et interaktivt non-login. Hvorfor det er sådan må Apple kunne svare på[^3]. Det betyder også at på min Mac, bliver først ~/.bash_profile kørt og ved logud (altså, når Terminalen lukkes) bliver så ~/.bash_logout eksekveret af systemet, resten af filerne (.bash_aliases, .bash_prompt og .osx) bliver så sourcet fra disse eller kørt manuelt.

### Filerne

~/.bash_profile - køres af køres af operativsystemet

    :::bash
    # .bash_profile
    # Executed for login bash shells

    # Add `~/bin` to the `$PATH`
    export PATH="$HOME/bin:$PATH";

    # don't put duplicate lines or lines starting with space in the history.
    # See bash(1) for more options
    HISTCONTROL=ignoreboth

    # append to the history file, don't overwrite it
    shopt -s histappend

    # for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
    HISTSIZE=1000
    HISTFILESIZE=2000

    # Load the shell dotfiles, and then some:
    # * ~/.path can be used to extend `$PATH`.
    # * ~/.extra can be used for other settings you don’t want to commit.
    for file in ~/.{bash_prompt,bash_aliases}; do
    	[ -r "$file" ] && [ -f "$file" ] && source "$file";
    done;
    unset file;

    # Enable bash completion
    if [ -f $(brew --prefix)/etc/bash_completion ]; then
        . $(brew --prefix)/etc/bash_completion
    fi

    # Add tab completion for SSH hostnames based on ~/.ssh/config, ignoring wildcards
    [ -e "$HOME/.ssh/config" ] && complete -o "default" -o "nospace" -W "$(grep "^Host" ~/.ssh/config | grep -v "[?*]" | cut -d " " -f2- | tr ' ' '\n')" scp sftp ssh;

~/.bash_aliases - køres fra ~/.bash_profile

    :::bash
    # .bash_aliases
    # Sourced by .bash_profile

    # Easier navigation
    alias ~="cd ~" # Home
    alias -- -="cd -" # Last used dir

    # Always start vmware horizon view in detached state directing standard out to /dev/null
    alias vmware-view="vmware-view </dev/null &>/dev/null &"
    # v for vmware-view
    alias v="vmware-view"

    # Source virtualenv
    alias venv="source ./venv/bin/activate"

    # Weeknumber
    alias week='date +%V'

    # Get OS X Software Updates, and Homebrew, and their installed packages
    alias update='sudo softwareupdate -i -a; brew update; brew upgrade --all; brew cleanup'

    # Show/hide hidden files in Finder
    alias show="defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder"
    alias hide="defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder"

    # Detect which `ls` flavor is in use
    if ls --color > /dev/null 2>&1; then # GNU `ls`
    	colorflag="--color"
    else # OS X `ls`
    	colorflag="-G"
    fi

    # List all files colorized in long format
    alias ll="ls -lF ${colorflag}"

    # List all files colorized in long format, including dot files
    alias la="ls -laF ${colorflag}"

    # List only directories
    alias lsd="ls -lF ${colorflag} | grep --color=never '^d'"

    # Always use color output for `ls`
    alias ls="command ls ${colorflag}"
    export LS_COLORS='no=00:fi=00:di=01;34:ln=01;36:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.gz=01;31:*.bz2=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.avi=01;35:*.fli=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.ogg=01;35:*.mp3=01;35:*.wav=01;35:'

~/.bash_prompt - køres fra ~/.bash_profile

    :::bash
    # .bash_profile
    # Sourced by .bash_profile

    # Shell prompt based on the Solarized Dark theme.
    # More or less by Mathias Bynens. Heavily inspired by @necolas’s prompt: https://github.com/necolas/dotfiles
    # iTerm → Profiles → Text → use 13pt Monaco with 1.1 vertical spacing.

    if [[ $COLORTERM = gnome-* && $TERM = xterm ]] && infocmp gnome-256color >/dev/null 2>&1; then
    	export TERM='gnome-256color';
    elif infocmp xterm-256color >/dev/null 2>&1; then
    	export TERM='xterm-256color';
    fi;

    prompt_git() {
    	local s='';
    	local branchName='';

    	# Check if the current directory is in a Git repository.
    	if [ $(git rev-parse --is-inside-work-tree &>/dev/null; echo "${?}") == '0' ]; then

    		# check if the current directory is in .git before running git checks
    		if [ "$(git rev-parse --is-inside-git-dir 2> /dev/null)" == 'false' ]; then

    			# Ensure the index is up to date.
    			git update-index --really-refresh -q &>/dev/null;

    			# Check for uncommitted changes in the index.
    			if ! $(git diff --quiet --ignore-submodules --cached); then
    				s+='+';
    			fi;

    			# Check for unstaged changes.
    			if ! $(git diff-files --quiet --ignore-submodules --); then
    				s+='!';
    			fi;

    			# Check for untracked files.
    			if [ -n "$(git ls-files --others --exclude-standard)" ]; then
    				s+='?';
    			fi;

    			# Check for stashed files.
    			if $(git rev-parse --verify refs/stash &>/dev/null); then
    				s+='$';
    			fi;

    		fi;

    		# Get the short symbolic ref.
    		# If HEAD isn’t a symbolic ref, get the short SHA for the latest commit
    		# Otherwise, just give up.
    		branchName="$(git symbolic-ref --quiet --short HEAD 2> /dev/null || \
    			git rev-parse --short HEAD 2> /dev/null || \
    			echo '(unknown)')";

    		[ -n "${s}" ] && s=" [${s}]";

    		echo -e "${1}${branchName}${blue}${s}";
    	else
    		return;
    	fi;
    }

    if tput setaf 1 &> /dev/null; then
    	tput sgr0; # reset colors
    	bold=$(tput bold);
    	reset=$(tput sgr0);
    	# Solarized colors, taken from http://git.io/solarized-colors.
    	black=$(tput setaf 0);
    	blue=$(tput setaf 33);
    	cyan=$(tput setaf 37);
    	green=$(tput setaf 64);
    	orange=$(tput setaf 166);
    	purple=$(tput setaf 125);
    	red=$(tput setaf 124);
    	violet=$(tput setaf 61);
    	white=$(tput setaf 15);
    	yellow=$(tput setaf 136);
    else
    	bold='';
    	reset="\e[0m";
    	black="\e[1;30m";
    	blue="\e[1;34m";
    	cyan="\e[1;36m";
    	green="\e[1;32m";
    	orange="\e[1;33m";
    	purple="\e[1;35m";
    	red="\e[1;31m";
    	violet="\e[1;35m";
    	white="\e[1;37m";
    	yellow="\e[1;33m";
    fi;

    # Highlight the user name when logged in as root.
    if [[ "${USER}" == "root" ]]; then
    	userStyle="${red}";
    else
    	userStyle="${orange}";
    fi;

    # Highlight the hostname when connected via SSH.
    if [[ "${SSH_TTY}" ]]; then
    	hostStyle="${bold}${red}";
    else
    	hostStyle="${yellow}";
    fi;

    # Set the terminal title to the current working directory.
    PS1="\[\033]0;\w\007\]";
    PS1+="\[${bold}\]\n"; # newline
    PS1+="\[${userStyle}\]\u"; # username
    PS1+="\[${white}\] @ ";
    PS1+="\[${hostStyle}\]\h"; # host
    PS1+="\[${white}\] in ";
    PS1+="\[${green}\]\w"; # working directory
    PS1+="\$(prompt_git \"${white} on ${violet}\")"; # Git repository details
    PS1+="\n";
    PS1+="\[${white}\]\$ \[${reset}\]"; # `$` (and reset color)
    export PS1;

    PS2="\[${yellow}\]→ \[${reset}\]";
    export PS2;

~/.bash_logout - køres af køres af operativsystemet

    :::bash
    # .bash_logout
    # Executed after logout of bash shells

    clear

~/.osx - håndkøres ved opsætning af ny Mac

    :::bash
    # .osx
    # Highly opinionated OS X specific configuration

    ###############################################################################
    # Installing apps                                                             #
    ###############################################################################

    # Install Xcode cli-tools
    xcode-select --install

    # Install Brew (http://brew.sh)
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

    # Install Caskroom (http://caskroom.io)
    brew install caskroom/cask/brew-cask

    # Install REAL python (including pip etc.)
    brew install python

    # Install missing unix components
    brew install ssh-copy-id
    brew install bash-completion

    # Install apps
    brew cask install hazel
    brew cask install 1password
    brew cask install textwrangler
    brew cask install dropbox
    brew cask install google-chrome
    brew cask install transmit
    brew cask install little-snitch


    ###############################################################################
    # Global settings / UI                                                        #
    ###############################################################################

    # Tap-to-click (logout and back in to activate):
    defaults -currentHost write -globalDomain com.apple.mouse.tapBehavior -int 1

    # Set highlight color to green
    defaults write NSGlobalDomain AppleHighlightColor -string "0.764700 0.976500 0.568600"

    # Hot corners
    # Possible values:
    #  0: no-op
    #  2: Mission Control
    #  3: Show application windows
    #  4: Desktop
    #  5: Start screen saver
    #  6: Disable screen saver
    #  7: Dashboard
    # 10: Put display to sleep
    # 11: Launchpad
    # 12: Notification Center
    # Top left screen corner → Put display to sleep
    defaults write com.apple.dock wvous-tl-corner -int 10
    defaults write com.apple.dock wvous-tl-modifier -int 0
    # Top right screen corner → Desktop
    defaults write com.apple.dock wvous-tr-corner -int 4
    defaults write com.apple.dock wvous-tr-modifier -int 0
    # Bottom left screen corner → Show application windows
    defaults write com.apple.dock wvous-bl-corner -int 3
    defaults write com.apple.dock wvous-bl-modifier -int 0
    # Bottom right screen corner → Mission Control
    defaults write com.apple.dock wvous-br-corner -int 2
    defaults write com.apple.dock wvous-br-modifier -int 0


    ###############################################################################
    # Safari & WebKit                                                             #
    ###############################################################################

    # Privacy: don’t send search queries to Apple
    defaults write com.apple.Safari UniversalSearchEnabled -bool false
    defaults write com.apple.Safari SuppressSearchSuggestions -bool true

    # Show the full URL in the address bar (note: this still hides the scheme)
    defaults write com.apple.Safari ShowFullURLInSmartSearchField -bool true

    # Prevent Safari from opening ‘safe’ files automatically after downloading
    defaults write com.apple.Safari AutoOpenSafeDownloads -bool false

    # Hide Safari’s bookmarks bar by default
    defaults write com.apple.Safari ShowFavoritesBar -bool false

    # Hide Safari’s sidebar in Top Sites
    defaults write com.apple.Safari ShowSidebarInTopSites -bool false

[^1]: Ren tekst, som kan læses på en hvilken som helst computer lavet siden 70'erne. I øvrigt samme format, som denne blog bliver skrevet i.
[^2]: Hvorfra nedenstående tabel da også er tyvstjålet.
[^3]: Da det - som sædvanen byder - er dem, der afviger fra standarden. *suk*
