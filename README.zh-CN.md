# 鏃ュ織鍒嗘瀽鍛戒护琛屽伐鍏?
[English](README.md)

鍒嗘瀽绾枃鏈棩蹇椾腑鐨勭骇鍒€丠TTP 鐘舵€佺爜銆佹椂闂磋寖鍥村拰閲嶅娑堟伅妯″紡銆?
## 涓昏鍔熻兘

- 缁熻 TRACE銆丏EBUG銆両NFO銆乄ARN銆丒RROR銆丆RITICAL 鍜?FATAL銆?- 姹囨€绘棩蹇椾腑鐨?HTTP 鐘舵€佺爜銆?- 鎶ュ憡鏈€鏃╁拰鏈€鏅氱殑 ISO 椋庢牸鏃堕棿鎴炽€?- 鏇挎崲鏃堕棿鍜屾暟瀛楀悗褰掑苟閲嶅娑堟伅銆?- 瀵煎嚭璇︾粏 JSON 鍜屾眹鎬?CSV 鎶ュ憡銆?- 鍙鍙栨棩蹇楋紝涓嶄慨鏀规垨鍒犻櫎婧愭枃浠躲€?
## 瀹夎

```bash
git clone https://github.com/jellywong343-sys/log-analyzer-cli.git
cd log-analyzer-cli
python -m pip install -e .
```

## 浣跨敤

```bash
log-analyze examples/application.log
log-analyze app.log server.log --top 20 --json report.json
log-analyze app.log --csv summary.csv
```

## 娴嬭瘯

```bash
python -m unittest discover -s tests -v
```

## 寮€婧愬崗璁?
MIT



