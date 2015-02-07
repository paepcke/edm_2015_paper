import os
import shutil
import sys
import tempfile

from video_footprint_index import VideoFootPrintIndex

# Given a course name, generate all that course's video
# heatmaps either using all learners' events, or only events
# from selected learners. 
#
# Set courseDisplayName to the desired course name triplet.
# If only use particular learners, fill the specialLearnersList
# with those learner IDs. Else make that array empty.
#
# Script will print the path of the result file when done.

#courseDisplayName = 'Medicine/HRP261/Winter2014'
courseDisplayName = 'Medicine/HRP262/Spring2014'
specialLearnersList = [
			# 'd9e40e111506cf299441abc35a56fb4bdac0daad', # HRP261
			# '8811cf97c75bedcdd46357d89a2a27be5ac15547',
			# 'd9dbe743c9cde774b3733eeddd3354780f18a057',
			# '862329793fdbcd666d660d9a9d2e3beceb07a0db',
			# '3128a1a01469c448a4749d006b0bd89cf8985181',
			# '4050598e2c5262ddd3a402f9031e5299dd228ef2',
			# 'fe1c91be4933b2ba7132b8d79499b4ee63827a14',
			# 'a9618d15d7f7aabfd07f7cae3b9e02f8366aa0c4',
			# 'b482f938743fd96d935df9bb8aadfd668ad11054',
			# '1f629a87b17ea62a0ee12f48e711fd856ec03af6',
			# '864bba9b886f435402d61ac6b403ac22df198085',
			# '2d7e2258582a10c4a7234386132b21436af5a43e',
			# '41376e75a9ccda4ab4c2be5a1b79458e399c5f1d',
			# '62c4488cd7208f918ecd1713d162529fa52c6741',
			# '7d1583a3170569c2bb8c4e5ed30f00c2e797ca92',
			# 'c03c625012511c3c4a46f3e0af45fe2faa6208c9',
			# '5fb78a6b40c0970e124fedd3f78ab8165b873df7',
			# 'a0d8ebac6d6716b9b23de452e013a3c73d91e7fc',
			# '6b09cfc1f45b4c3edc7526bf84db131f9ec24996',
			# '5485ba4a90ce344866751882f3299ba8207473c6'

			'2d7e2258582a10c4a7234386132b21436af5a43e', # HRP262
			'd9e40e111506cf299441abc35a56fb4bdac0daad',
			'9cc0909cb4a4c2f2c61b48c85ee033dd2d717487',
			'aded057672c15ffc6e9d753a89067e704e7c838b',
			'fe1c91be4933b2ba7132b8d79499b4ee63827a14',
			'1c1ce9a7e0b972d1da86b445e90d087349d298f9',
			'05368cdab761a27aa48461b0d67164958fbc237e',
			'6b09cfc1f45b4c3edc7526bf84db131f9ec24996',
			'b482f938743fd96d935df9bb8aadfd668ad11054',
			'3849f32b31b58eb7943876b78bb5df39039fd6f6',
			'7d1583a3170569c2bb8c4e5ed30f00c2e797ca92',
			'9774fdbeadb3f6a104d170718e5cc61ad9f22788',
			'a0f43a4284e6347a0b929d64f6ab465053fe8c5d',
			'862329793fdbcd666d660d9a9d2e3beceb07a0db',
			'3128a1a01469c448a4749d006b0bd89cf8985181',
			'41376e75a9ccda4ab4c2be5a1b79458e399c5f1d',
			'62c4488cd7208f918ecd1713d162529fa52c6741',
			'ccc2cd95297a483d6edf0498088f0c0fb9e5a31d',
			'a0d4adbda324336524bb359e0afc7628d8b4f9ec',
			'864bba9b886f435402d61ac6b403ac22df198085',

                        ]
footprintIndex = VideoFootPrintIndex(indexSavePath=None,
				     viewEventsCSVFile=None,
                                     specialLearnersList=specialLearnersList)

#footprintIndex = VideoFootPrintIndex(indexSavePath=None,
#				     viewEventsCSVFile=None)


footprintIndex.computeFootprints(courseDisplayName)
resultFilePrefix = '/tmp/heatMaps_%s' % courseDisplayName.replace('/','_')
if len(specialLearnersList) == 0:
  heatMapResultFile = '%s_AllLearners.csv' % resultFilePrefix
else:
  heatMapResultFile = '%s_SpecialLearners.csv' % resultFilePrefix

footprintIndex.videoHeatAll(heatMapResultFile)

if len(specialLearnersList) == 0:
  print("Heatmaps all learners are in %s" % heatMapResultFile)
else:
  print("Heatmaps special learners are in %s" % heatMapResultFile)




