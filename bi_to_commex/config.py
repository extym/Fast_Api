API_KEY = "NRhQ5e2hdBnMkCrNUp75QAUwvxlRLdTMFunuimInzviKJx8ST4s10qewC7LWbMFb"  #"FHvyWlnMKTpTKjCRPrHlfA0FpEA9zzxDZmvA7Q2cKQvxpJMWR73qe6O5CcmqDMMa"
API_SECRET = "rlZNIyWEoDUyWSCmkD8FJoz42sbDHrNWvVcU4spaPQUTE8bUzBm7bDIDCzsSSFWg"  #"GHzDCTrdAtY5L3N21gHa5uuj9KS9Snl3bw7E2sD7A8u8m3bDOIjUP85xWcmnx8tD"

tps = {
    "BTCUSDT": {
        "TP": {
            "[0.02, 0.02, 0.2]": 4.0,
        }
    }
}

couples = {
    "BTC": {
        "enable": "ON",
        "ticker": "BTCUSDT",
        "timeFrame": "1d",
        "saving_funds": False,
	    "startBalance": 100,
        "multiplier_size": 1,
        "ticks_to_open": 1,

        "size_steps": [1],
        "steps": [1],

        "SAR": [0.02, 0.02, 0.2],
        "SL": 5,
        "LEV": 2
    }
}


