
# Export guake settings
guakeexp() { guake --save-preferences $1; }

# Import guake settings
guakeimp() { guake --restore-preferences $1; }
