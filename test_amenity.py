# coding: utf-8

import osmtest
import re

# 不顯示 stack trace
__unittest = True

class AmenityTestCase(osmtest.OsmTestCase):

	## point 命名有廁所，但是 amenity 為 NULL
	def test01_toilets_without_amenity(self):
		sql = """
			SELECT osm_id,name,amenity FROM planet_osm_point
			WHERE name LIKE '%廁所%' AND amenity IS NULL
		"""
		rows = self.query(sql)
		if len(rows)>0:
			summary = self.get_osmid_summary(rows)
			msg = '找到沒標記 amenity 的廁所 (%s)' % summary
			self.fail(msg)

	## amenity 為 toilet
	def test02_toilets_as_toilet(self):
		sql = """
			SELECT osm_id,name,amenity FROM planet_osm_point
			WHERE amenity LIKE '%toilet%' AND amenity!='toilets'
		"""
		rows = self.query(sql)
		if len(rows)>0:
			summary = self.get_osmid_summary(rows)
			msg = '找到 amenity 誤標記成 toilet 的廁所 (%s)' % summary
			self.fail(msg)

	## 沒命名也沒說明用途的地點 (高達 37520 個，先擱著晚點再測)
	def test03_invalid_points(self):
		sql = "SELECT count(*) FROM planet_osm_point WHERE amenity IS NULL AND name IS NULL"
		pass

	## amenity 疑似錯誤的地點
	def test04_bad_amenities(self):
		sql = '''
			SELECT MIN(osm_id) osm_id, amenity, COUNT(*) cnt FROM planet_osm_point
			WHERE amenity IS NOT NULL
			GROUP BY amenity ORDER BY cnt DESC
		'''
		rows = self.query(sql)

		pat = re.compile('^[a-z][a-z_]{0,28}[a-z]$')
		bad_amenities = []
		for r in rows:
			if pat.match(r['amenity']) is None:
				bad_amenities.append(r['amenity'])

		if len(bad_amenities) > 0:
			msg = '找到疑似錯誤的 amenity (%s)' % ', '.join(bad_amenities)
			self.fail(msg)
