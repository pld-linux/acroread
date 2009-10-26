#!/bin/sh
if [ "$1" = "--with" -a "$2" = "license_agreement" ]; then
	tmp=$(mktemp -d)
	SRPMDIR=`rpm --define "_topdir $tmp" --eval "%{_srcrpmdir}"`
	BUILDDIR=`rpm --define "_topdir $tmp" --eval "%{_builddir}"`
	RPMDIR=`rpm --define "_topdir $tmp" --eval "%{_rpmdir}"`
	PACKAGEDIR="$tmp/packages/acroread"
	mkdir -p $SRPMDIR $RPMDIR $BUILDDIR $PACKAGEDIR

	if echo "$3" | grep '\.src\.rpm$' >/dev/null; then
		(
		if echo "$3" | grep '://' >/dev/null; then
			cd $SRPMDIR
			wget --passive-ftp -t0 "$3"
		else
			cp -f "$3" $SRPMDIR
		fi
		rpm2cpio `basename "$3"` | ( cd $PACKAGEDIR; cpio -i @BASE_NAME@.spec )
		if [ '@COPYSOURCES@' != '@'COPYSOURCES'@' ]; then
			rpm2cpio `basename "$3"` | ( cd $PACKAGEDIR; cpio -i @COPYSOURCES@ )
		fi
	   	)
	else
		cp -i "$3" $PACKAGEDIR || exit 1
		if [ '@COPYSOURCES@' != '@'COPYSOURCES'@' ]; then
			for i in @COPYSOURCES@; do
				cp -i @DATADIR@/$i $PACKAGEDIR/$i || exit 1
			done
		fi
	fi
	( cd $PACKAGEDIR
	nd=
	if [ '@USE_DISTFILES@' = 'no' ]; then
		nd=-nd
	fi
	/usr/bin/builder --define _topdir $tmp --define _binary_payload w1.gzdio $nd -nm -nc -ncs --with license_agreement --target @TARGET_CPU@ @BASE_NAME@.spec
	if [ "$?" -ne 0 ]; then
		exit 2
	fi
	RPMNAMES="$RPMDIR/@BASE_NAME@-@VERSION@-@RELEASE@wla.@TARGET_CPU@.rpm"
	rpm -Uhv $RPMNAMES || echo -e "Install manually the file(s):\n   $RPMNAMES" )
else
	if [ "@LICENSE@" != '@'LICENSE'@' ]; then
		cat @LICENSE@
		echo "
If you accept the above license rebuild the package using:
"
	else
		echo "
License issues made us not to include inherent files into
this package by default. If you want to create full working
package please build it with the following command:
"
	fi
	echo "$0 --with license_agreement @SPECFILE@"
fi
