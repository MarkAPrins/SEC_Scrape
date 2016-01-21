import urllib
import re
import sqlite3
import decimal

conn = sqlite3.connect('BDC_DB.sqlite')
cur = conn.cursor()

#this allows me to find nth occurrence of a substring and is used for TPVG; source: stackoverflow
def find_nth(s, x, n):
    i = -1
    for _ in range(n):
        i = s.find(x, i + len(x))
        if i == -1:
            break
    return i


def HTGC(x):

	html = urllib.urlopen(x).read()

	begin = re.findall('For The Quarterly Period Ended(.+<)', html)
	DATE = begin[0].rstrip('<')
	print 'For the Quarter Ended:', DATE

	atpos = html.find('Net investment income')
	string = html[atpos : atpos+1000]
	begin = re.findall('normal;">([^>][0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NII = float(end.replace(',',''))

	atpos = html.find('Total investment income')
	string = html[atpos : atpos+1000]
	begin = re.findall('normal;">([^>][0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TII = float(end.replace(',',''))

	atpos = html.find('Total assets')
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TA = float(end.replace(',',''))

	atpos = html.find('Total liabilities')
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TL = float(end.replace(',',''))
	
	NAV = TA - TL

	atpos = html.find('Total net assets')
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TNA = float(end.replace(',',''))
	
	atpos = html.find('Net asset value per share')
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NAVShare = float(end.replace(',',''))
	
	cur.execute('''INSERT OR REPLACE INTO QUARTERLY_DATA
		(company_id, PERIOD_END_DATE, NET_INVESTMENT_INCOME, TOTAL_INVESTMENT_INCOME, TOTAL_ASSETS, TOTAL_LIABILITIES, NET_ASSET_VALUE, TOTAL_NET_ASSETS, NET_ASSET_VALUE_PER_SHARE)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''',
		(1, DATE, NII, TII, TA, TL, NAV, TNA, NAVShare ) )
		
	conn.commit()
	
	
def TCPC(x):

	html = urllib.urlopen(x).read()

	begin = re.findall('For the Quarter Ended(.+<)', html)
	DATE = begin[0].rstrip('<')
	print 'For the Quarter Ended:', DATE

	atpos = html.find('Net investment income')
	string = html[atpos : atpos+1000]
	begin = re.findall('FONT-SIZE: 10pt">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NII = round(float(end.replace(',',''))/1000,0)

	atpos = html.find('Total investment income')
	string = html[atpos : atpos+1000]
	begin = re.findall('FONT-SIZE: 10pt">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TII = round(float(end.replace(',',''))/1000,0)

	atpos = html.find('Total assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('FONT-SIZE: 10pt">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TA = round(float(end.replace(',',''))/1000,0)

	atpos = html.find('Total liabilities')
	string = html[atpos : atpos+1000]
	begin = re.findall('FONT-SIZE: 10pt">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TL = round(float(end.replace(',',''))/1000,0)

	NAV = TA - TL
	
	atpos = html.find('Net assets applicable to common shareholders')
	string = html[atpos : atpos+1000]
	#notice that the below signature is different
	begin = re.findall('FONT-WEIGHT: bold">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TNA = round(float(end.replace(',',''))/1000,0)

	atpos = html.find('Net assets per share')
	string = html[atpos : atpos+1000]
	begin = re.findall('FONT-SIZE: 10pt">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NAVShare = float(end.replace(',',''))

	cur.execute('''INSERT OR REPLACE INTO QUARTERLY_DATA
		(company_id, PERIOD_END_DATE, NET_INVESTMENT_INCOME, TOTAL_INVESTMENT_INCOME, TOTAL_ASSETS, TOTAL_LIABILITIES, NET_ASSET_VALUE, TOTAL_NET_ASSETS, NET_ASSET_VALUE_PER_SHARE)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''',
		(2, DATE, NII, TII, TA, TL, NAV, TNA, NAVShare ) )
		
	conn.commit()


def TCRD(x):

	html = urllib.urlopen(x).read()

	begin = re.findall('THE QUARTER ENDED(.+?<)', html)
	DATE = begin[0].rstrip('<')
	print 'For the Quarter Ended:', DATE

	atpos = html.find('Net investment income')
	string = html[atpos : atpos+1000]
	begin = re.findall('Times New Roman" SIZE="2">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NII = float(end.replace(',',''))

	atpos = html.find('Total investment income')
	string = html[atpos : atpos+1000]
	begin = re.findall('Times New Roman" SIZE="2">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TII = float(end.replace(',',''))

	atpos = html.find('Total assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('Times New Roman" SIZE="2">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TA = float(end.replace(',',''))

	atpos = html.find('Total liabilities')
	string = html[atpos : atpos+1000]
	begin = re.findall('Times New Roman" SIZE="2">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TL = float(end.replace(',',''))

	NAV = TA - TL
	
	atpos = html.find('Total net assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('Times New Roman" SIZE="2">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TNA = float(end.replace(',',''))

	atpos = html.find('Net asset value per share')
	string = html[atpos : atpos+1000]
	begin = re.findall('Times New Roman" SIZE="2">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NAVShare = float(end.replace(',',''))

	cur.execute('''INSERT OR REPLACE INTO QUARTERLY_DATA
		(company_id, PERIOD_END_DATE, NET_INVESTMENT_INCOME, TOTAL_INVESTMENT_INCOME, TOTAL_ASSETS, TOTAL_LIABILITIES, NET_ASSET_VALUE, TOTAL_NET_ASSETS, NET_ASSET_VALUE_PER_SHARE)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''',
		(3, DATE, NII, TII, TA, TL, NAV, TNA, NAVShare ) )
		
	conn.commit()
		

def KCAP(x):

	html = urllib.urlopen(x).read()

	begin = re.findall('For the quarterly period ended(.+?<)', html)
	DATE = begin[0].rstrip('<')
	print 'For the Quarter Ended:', DATE
	
	atpos = html.find('Net Investment Income')
	string = html[atpos : atpos+1000]
	begin = re.findall('text-align: right">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NII = round(float(end.replace(',',''))/1000,0)

	atpos = html.find('Total investment income')
	string = html[atpos : atpos+1000]
	begin = re.findall('text-align: right">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TII = round(float(end.replace(',',''))/1000,0)

	atpos = html.find('Total Assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('text-align: right">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TA = round(float(end.replace(',',''))/1000,0)

	atpos = html.find('Total Liabilities')
	string = html[atpos : atpos+1000]
	begin = re.findall('text-align: right">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TL = round(float(end.replace(',',''))/1000,0)

	NAV = (TA - TL)
	
	#NOT SURE THIS IS THE RIGHT METRIC FOR TOTAL NET ASSETS
	atpos = html.find('Total Liabilities and Stockholders')
	string = html[atpos : atpos+1000]
	begin = re.findall('text-align: right">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TNA = round(float(end.replace(',',''))/1000,0)

	atpos = html.find('NET ASSET VALUE PER COMMON SHARE')
	string = html[atpos : atpos+1000]
	begin = re.findall('text-align: right">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NAVShare = float(end.replace(',',''))

	cur.execute('''INSERT OR REPLACE INTO QUARTERLY_DATA
		(company_id, PERIOD_END_DATE, NET_INVESTMENT_INCOME, TOTAL_INVESTMENT_INCOME, TOTAL_ASSETS, TOTAL_LIABILITIES, NET_ASSET_VALUE, TOTAL_NET_ASSETS, NET_ASSET_VALUE_PER_SHARE)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''',
		(4, DATE, NII, TII, TA, TL, NAV, TNA, NAVShare ) )
		
	conn.commit()
		

def MAIN(x):

	html = urllib.urlopen(x).read()

	begin = re.findall('For the quarterly period ended(.+?<)', html)
	middle = begin[0].rstrip('<')
	DATE = middle.replace('&nbsp;',' ')
	print 'For the Quarter Ended:', DATE
	
	atpos = html.find('NET INVESTMENT INCOME')
	string = html[atpos : atpos+1000]
	begin = re.findall('<FONT SIZE=1>([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NII = float(end.replace(',',''))

	atpos = html.find('Total investment income')
	string = html[atpos : atpos+1000]
	begin = re.findall('<FONT SIZE=1>([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TII = float(end.replace(',',''))

	atpos = html.find('Total assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('<FONT SIZE=1>([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TA = float(end.replace(',',''))

	atpos = html.find('Total liabilities')
	string = html[atpos : atpos+1000]
	begin = re.findall('<FONT SIZE=1>([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TL = float(end.replace(',',''))

	NAV = TA - TL
	
	atpos = html.find('Total net assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('<FONT SIZE=1>([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TNA = float(end.replace(',',''))

	atpos = html.find('NET ASSET VALUE PER SHARE')
	string = html[atpos : atpos+1000]
	begin = re.findall('<FONT SIZE=1>([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NAVShare = float(end.replace(',',''))

	cur.execute('''INSERT OR REPLACE INTO QUARTERLY_DATA
		(company_id, PERIOD_END_DATE, NET_INVESTMENT_INCOME, TOTAL_INVESTMENT_INCOME, TOTAL_ASSETS, TOTAL_LIABILITIES, NET_ASSET_VALUE, TOTAL_NET_ASSETS, NET_ASSET_VALUE_PER_SHARE)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''',
		(5, DATE, NII, TII, TA, TL, NAV, TNA, NAVShare ) )
		
	conn.commit()
	

def ARCC(x):

	html = urllib.urlopen(x).read()

	begin = re.findall('For the quarterly period ended(.+?<)', html)
	middle = begin[0].rstrip('<')
	DATE = middle.replace('&nbsp;',' ')
	print 'For the Quarter Ended:', DATE
	
	atpos = html.find('NET INVESTMENT   INCOME<')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10.0pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NII = float(end.replace(',',''))

	atpos = html.find('Total investment   income')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10.0pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TII = float(end.replace(',',''))

	atpos = html.find('Total assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10.0pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TA = float(end.replace(',',''))

	atpos = html.find('Total   liabilities')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10.0pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TL = float(end.replace(',',''))

	NAV = TA - TL
	
	atpos = html.find('Total   stockholders')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10.0pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TNA = float(end.replace(',',''))

	atpos = html.find('NET   ASSETS PER SHARE')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10.0pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NAVShare = float(end.replace(',',''))

	cur.execute('''INSERT OR REPLACE INTO QUARTERLY_DATA
		(company_id, PERIOD_END_DATE, NET_INVESTMENT_INCOME, TOTAL_INVESTMENT_INCOME, TOTAL_ASSETS, TOTAL_LIABILITIES, NET_ASSET_VALUE, TOTAL_NET_ASSETS, NET_ASSET_VALUE_PER_SHARE)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''',
		(6, DATE, NII, TII, TA, TL, NAV, TNA, NAVShare ) )
		
	conn.commit()
	
		
def AINV(x):

	html = urllib.urlopen(x).read()

	atpos = html.find('FOR THE QUARTER ENDED')
	string = html[atpos : atpos+500]
	begin = re.findall(':bold;">([A-Z].+?<)', string)
	DATE = begin[0].rstrip('<')
	if '&#160;' in DATE:
		DATE = DATE.replace('&#160;',' ')
	if '&nbsp;' in DATE:
		DATE = DATE.replace('&nbsp;',' ')
	print 'For the Quarter Ended:', DATE
	
	atpos = html.find('Net Investment Income')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NII = float(end.replace(',',''))

	atpos = html.find('Total Investment Income')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TII = float(end.replace(',',''))

	atpos = html.find('Total Assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TA = float(end.replace(',',''))

	atpos = html.find('Total Liabilities')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TL = float(end.replace(',',''))

	NAV = TA - TL
	
	atpos = html.find('Total Net Assets')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TNA = float(end.replace(',',''))

	atpos = html.find('Net asset value per share')
	string = html[atpos : atpos+1000]
	begin = re.findall('font-size:10pt;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NAVShare = float(end.replace(',',''))

	cur.execute('''INSERT OR REPLACE INTO QUARTERLY_DATA
		(company_id, PERIOD_END_DATE, NET_INVESTMENT_INCOME, TOTAL_INVESTMENT_INCOME, TOTAL_ASSETS, TOTAL_LIABILITIES, NET_ASSET_VALUE, TOTAL_NET_ASSETS, NET_ASSET_VALUE_PER_SHARE)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''',
		(7, DATE, NII, TII, TA, TL, NAV, TNA, NAVShare ) )
		
	conn.commit()
		
def TPVG(x):

	html = urllib.urlopen(x).read()

	begin = re.findall('FOR THE QUARTERLY PERIOD ENDED(.+<)', html)
	DATE = begin[0].rstrip('<')
	print 'For the Quarter Ended:', DATE

	atpos = find_nth(html, 'Net Investment Income', 1)
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NII = float(end.replace(',',''))

	atpos = html.find('Total investment and other income')
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TII = float(end.replace(',',''))

	atpos = html.find('Total Assets')
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TA = float(end.replace(',',''))

	atpos = html.find('Total Liabilities')
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TL = float(end.replace(',',''))
	
	NAV = TA - TL

	atpos = find_nth(html, 'Net Assets', 2)
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	TNA = float(end.replace(',',''))
	
	atpos = html.find('Net Asset Value per Share')
	string = html[atpos : atpos+1500]
	begin = re.findall('normal;">([0-9].*?<)', string)
	end = begin[0].rstrip('<')
	NAVShare = float(end.replace(',',''))
	
	cur.execute('''INSERT OR REPLACE INTO QUARTERLY_DATA
		(company_id, PERIOD_END_DATE, NET_INVESTMENT_INCOME, TOTAL_INVESTMENT_INCOME, TOTAL_ASSETS, TOTAL_LIABILITIES, NET_ASSET_VALUE, TOTAL_NET_ASSETS, NET_ASSET_VALUE_PER_SHARE)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ? )''',
		(8, DATE, NII, TII, TA, TL, NAV, TNA, NAVShare ) )
		
	conn.commit()
		




#HTGC('https://www.sec.gov/Archives/edgar/data/1280784/000156459015009663/htgc-10q_20150930.htm')
#TCPC('https://www.sec.gov/Archives/edgar/data/1370755/000156761915001455/s001085x1_form10q.htm')
#TCRD('https://www.sec.gov/Archives/edgar/data/1464963/000119312515368373/d99302d10q.htm')
#KCAP('https://www.sec.gov/Archives/edgar/data/1372807/000114420415062758/v423552_10q.htm')
#MAIN('https://www.sec.gov/Archives/edgar/data/1396440/000104746915008405/a2226431z10-q.htm')
#ARCC('https://www.sec.gov/Archives/edgar/data/1287750/000110465915075535/a15-17976_110q.htm')
#AINV('https://www.sec.gov/Archives/edgar/data/1278752/000127875215000019/ainv-2015930x10q.htm')	
#TPVG('https://www.sec.gov/Archives/edgar/data/1580345/000156459015010370/tpvg-10q_20150930.htm')	
