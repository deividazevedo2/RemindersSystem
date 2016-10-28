#!/usr/bin/env python
# -*- coding: utf-8 -*-
import AnaliseDeComentarios

comentario = 'This issue is different from  IKSWL-1565 IKSWL-1565 is bp-tool mode,  in bp tool mode,even if secure hardware mode' \
             '([ro.boot.secure_hardware = 1) adb port is eanbled,this is not allowed. this issue in normal mode and not bp tool mode. ' \
             'Now cedric in  secure hardware mode  disable adb port.  in usr mode and not  secure hardware mode ,if adb can work，must  ' \
             'confirm “Always allow from this computer” from popup. so I dont think this is BSP issue, the following  is a similar issue, pls ' \
             '[~huanghc1] assign someone further analysis,thanks! https://idart.mot.com/browse/IKSWL-1139'

pattern = '，'
s = AnaliseDeComentarios.BoyerMooreHorspool(pattern.upper(), comentario.upper())

print s