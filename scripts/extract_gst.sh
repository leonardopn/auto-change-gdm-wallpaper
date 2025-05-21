#!/bin/sh

gst=/usr/share/gnome-shell/gnome-shell-theme.gresource
workdir=$1/shell-theme

if ! command -v gresource >/dev/null 2>&1; then
	echo "gresource is not installed. Please install it and try again."
	exit 1
fi

for r in $(gresource list $gst); do
	r=${r#\/org\/gnome\/shell/}
	if [ ! -d $workdir/${r%/*} ]; then
		mkdir -p $workdir/${r%/*}
	fi
done

for r in $(gresource list $gst); do
	gresource extract $gst $r >$workdir/${r#\/org\/gnome\/shell/}
done
