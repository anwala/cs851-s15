Assignment1.py
	- Retrieves links in tweets, resolves redirections
downloadHTML.py
	- downloads HTML texts of URIs in unique_originalLinksFile.txt and saves into RawHtml folder
histogramAndGraph.r
	- generates charts
https://github.com/HanySalahEldeen/CarbonDate
	- For Carbon dating URIs
originalLinksFile.txt
	- Raw data with duplicates
	<TWEET ID, URI, REDIRECTION COUNT, [REDIRECTION CODES], TWEET CREATED AT>
unique_originalLinksFile.txt
	- Raw data no duplicates
	<TWEET ID, URI, REDIRECTION COUNT, [REDIRECTION CODES], TWEET CREATED AT>
final_cd_unique_originalLinksFile.txt
	- Raw data no duplicates, with estimated creation dates
	<TWEET ID, URI, REDIRECTION COUNT, [REDIRECTION CODES], TWEET CREATED AT, ESTIMATED CREATED DATE>
REDIRECTION_COUNT_FREQUENCY.txt
	- contains redirection data for plot
STATUS_CODE_FREQUENCY.txt
	- contains HTTP status code data for plot
DELTA_DAYS.txt
	- contains estimated creation date derived from carbon dating


