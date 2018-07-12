DIMEN_AVG_ITEMS = [
    "ROUND(dimen1Avg, 2)", "ROUND(dimen2Avg, 2)", "ROUND(dimen3Avg, 2)", "ROUND(dimen4Avg, 2)",
    "ROUND(dimen5Avg, 2)", "ROUND(dimen6Avg, 2)", "ROUND(dimen7Avg, 2)", "ROUND(dimen8Avg, 2)",
    "ROUND(dimen9Avg, 2)", "ROUND(dimen10Avg, 2)", "ROUND(dimen11Avg, 2)", "ROUND(dimen12Avg, 2)",
    "ROUND(dimen13Avg, 2)", "ROUND(dimen14Avg, 2)", "ROUND(dimen15Avg, 2)", "ROUND(dimen16Avg, 2)",
]

DIMEN_RATIO_ITEMS = [
    "ROUND(dimen1Ratio * 100, 2)", "ROUND(dimen2Ratio * 100, 2)", "ROUND(dimen3Ratio * 100, 2)",
    "ROUND(dimen4Ratio * 100, 2)", "ROUND(dimen5Ratio * 100, 2)", "ROUND(dimen6Ratio * 100, 2)",
    "ROUND(dimen7Ratio * 100, 2)", "ROUND(dimen8Ratio * 100, 2)", "ROUND(dimen9Ratio * 100, 2)",
    "ROUND(dimen10Ratio * 100, 2)", "ROUND(dimen11Ratio * 100, 2)", "ROUND(dimen12Ratio * 100, 2)",
    "ROUND(dimen13Ratio * 100, 2)", "ROUND(dimen14Ratio * 100, 2)", "ROUND(dimen15Ratio * 100, 2)",
    "ROUND(dimen16Ratio * 100, 2)",
]

DIMEN_RANK_ITEMS = [
    "dimen1Rank", "dimen2Rank", "dimen3Rank", "dimen4Rank",
    "dimen5Rank", "dimen6Rank", "dimen7Rank", "dimen8Rank",
    "dimen9Rank", "dimen10Rank", "dimen11Rank", "dimen12Rank",
    "dimen13Rank", "dimen14Rank", "dimen15Rank", "dimen16Rank",
]

DIMEN_DESC_ITEMS = [
    "dimen1Des", "dimen2Des", "dimen3Des", "dimen4Des",
    "dimen5Des", "dimen6Des", "dimen7Des", "dimen8Des",
    "dimen9Des", "dimen10Des", "dimen11Des", "dimen12Des",
    "dimen13Des", "dimen14Des", "dimen15Des", "dimen16Des",
]

DIMEN_RANK_DIFF_ITEMS = [
    "font.dimen1Rank - behind.dimen1Rank", "font.dimen2Rank - behind.dimen2Rank",
    "font.dimen3Rank - behind.dimen3Rank", "font.dimen4Rank - behind.dimen4Rank",
    "font.dimen5Rank - behind.dimen5Rank", "font.dimen6Rank - behind.dimen6Rank",
    "font.dimen7Rank - behind.dimen7Rank", "font.dimen8Rank - behind.dimen8Rank",
    "font.dimen9Rank - behind.dimen9Rank", "font.dimen10Rank - behind.dimen10Rank",
    "font.dimen11Rank - behind.dimen11Rank", "font.dimen12Rank - behind.dimen12Rank",
    "font.dimen13Rank - behind.dimen13Rank", "font.dimen14Rank - behind.dimen14Rank",
    "font.dimen15Rank - behind.dimen15Rank", "font.dimen16Rank - behind.dimen16Rank",
]

LINE_25_60_85_ITEMS = ["line25", "line60", "line85"]

NULL_ITEM = "''"
NUM_ITEM = "num_nz"
SUM_ITEM = "sum"
AVG_ITEM = 'ROUND(avg, 2)'
RANK_ITEM = 'rank'
COUNT_ITEM = 'COUNT(*)'
AVG_RATIO_ITEM = 'ROUND(avg / %d, 2)'

AVG_NULL_ITEM = [AVG_ITEM, NULL_ITEM]
AVG_RANK_ITEM = [AVG_ITEM, RANK_ITEM]
