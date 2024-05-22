#!/bin/env bash
set -u

ENCODER=$1
INPUT_FILE=$2
CFG_FILE=$3
SOURCE_WDT=$4
SOURCE_HGT=$5
FRAME_RATE=$6
INPUT_BIT_DEPTH=$7

echo "QP,YUV_PSNR,Bytes"
for QP in 22 27 32 37
do
	LOG=qp${QP}.log
	${ENCODER} \
		-i ${INPUT_FILE} \
		-c ${CFG_FILE} \
		-f 9 \
		-q ${QP} \
		-wdt ${SOURCE_WDT} \
		-hgt ${SOURCE_HGT} \
		-fr ${FRAME_RATE} \
		--InputBitDepth=${INPUT_BIT_DEPTH} \
		--Level=2.1 \
		> ${LOG}
	YUV_PSNR=`sed -n -e '/SUMMARY/,+2p' ${LOG} \
		| tail -1 \
		| awk -e '{print $7}'`
	BYTES=`sed -n \
		-e 's/Bytes written to file: \([0-9]*\) .*/\1/p' \
		${LOG}`
	echo "${QP},${YUV_PSNR},${BYTES}"
done
