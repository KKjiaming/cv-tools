from labelme_related import labelme_tools
from stastic_related import stastic

folder_path = "/dataset/result/asset_detect_v0.6.0/巡检测试集/交通资产测试集/quchong/2023-2-21-new"
lm_tool = labelme_tools.LabelMan()
# st_tool = stastic.Static()

tracked_area, untracked_area = lm_tool.statistic_tacking(folder_path)
# st_tool.draw_distribution_picture( untracked_area,tracked_area,save_folder = "output/12fps-new")
