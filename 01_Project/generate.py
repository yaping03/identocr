# -*- coding: utf-8 -*-

import os
import sys
import xlsxwriter
import datetime

# edit by yelong
#def gen_excel(org_datetime_path,datetimestr,org,exams,contents,measures,managers,entities):
def gen_excel(org_datetime_path,datetimestr,org,exams,contents,measures,managers,entities,teamWeight):

    for exam in exams:

        if exam.name == u'领导班子年度综合考评':
            # add by yelong
            if teamWeight == None:
                continue
            if teamWeight.weight == 0:
                continue

            workbook = xlsxwriter.Workbook(os.path.join(org_datetime_path, u'班子.xlsx'))

            row_min_height = 6
            row_max_height = 12
            row_title_height = 28
            row_subtitle_height = 18

            row_index = 0

            col_min_width = 1.0
            col_max_width = 2.4

            col_index = 0
            
            for entity in entities:
                worksheet = workbook.add_worksheet(u'班子'+'_'+entity.name)

                # 0行 空白
                row_index = 0
                col_index = 0
                worksheet.set_row(row_index,row_min_height)

                # 1行 1-30列 标题 司属单位领导班子综合考核评价表（x票）
                row_index = row_index + 1
                worksheet.set_row(row_index,row_title_height)

                title = u'司属单位领导班子综合考核评价表' + ' ' + u'（' + entity.name + u'）'
                title_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':18})
                worksheet.merge_range(row_index, 1, row_index, 30, title, title_format)

                # 2行 空白
                row_index = row_index + 1
                worksheet.set_row(row_index,row_min_height)

                # 3行 1-20列 单位  21-30 日期
                row_index = row_index + 1
                worksheet.set_row(row_index,row_subtitle_height)

                org_title = u'单位名称：' + org.short_name
                org_format = workbook.add_format({'align':'left','valign':'vcenter','font_size':11})
                worksheet.merge_range(row_index, 1, row_index, 20, org_title, org_format)

                datetime_title = u'考评年度：' + datetimestr
                datetime_format = workbook.add_format({'align':'right','valign':'vcenter','font_size':11})
                worksheet.merge_range(row_index, 21, row_index, 30, datetime_title, datetime_format)

                # 4行 空白
                row_index = row_index + 1
                worksheet.set_row(row_index,row_min_height)
                                                                                                            
                # 5-8行 表格标题 [大小大小] 1-4 考评内容 5-9 考评指标 10-30 评 价 分 值
                row_index = row_index + 1
                row_index_start = row_index
                worksheet.set_row(row_index,row_max_height)
                row_index = row_index + 1
                worksheet.set_row(row_index,row_min_height)
                row_index = row_index + 1
                worksheet.set_row(row_index,row_max_height)
                row_index = row_index + 1
                row_index_end = row_index
                worksheet.set_row(row_index,row_min_height)

                grid_title_content = u'考评\n内容'
                grid_title_content_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':14,'text_wrap':True,'left':2,'left_color':'#fd1d1d','top':2,'top_color':'#fd1d1d'})
                worksheet.merge_range(row_index_start, 1, row_index_end, 4, grid_title_content, grid_title_content_format)

                grid_title_measure = u'考评指标'
                grid_title_measure_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':14,'top':2,'top_color':'#fd1d1d','left':1,'left_color':'#fd1d1d','right':1,'right_color':'#fd1d1d'})
                worksheet.merge_range(row_index_start, 5, row_index_end, 9, grid_title_measure, grid_title_measure_format)

                grid_title_score = u'评 价 分 值'
                grid_title_score_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':14,'top':2,'top_color':'#fd1d1d','right':2,'right_color':'#fd1d1d'})
                worksheet.merge_range(row_index_start, 10, row_index_end, 30, grid_title_score, grid_title_score_format)

                # 9-N 表格内容

                current_contents = filter(lambda c: c.exam_id==exam.id,contents)
                for ci,content in enumerate(current_contents):
                    content_index_start = row_index + 1

                    current_measures = filter(lambda m: m.exam_content_id==content.id,measures)
                    for mi,measure in enumerate(current_measures):
                        # 9-13行 指标 [大小大小大] 1-4 考评内容 5-9 考评指标 10-30 评 价 分 值
                        row_index = row_index + 1
                        row_index_start = row_index
                        worksheet.set_row(row_index,row_max_height)
                        row_index = row_index + 1
                        worksheet.set_row(row_index,row_min_height)
                        row_index = row_index + 1
                        worksheet.set_row(row_index,row_max_height)
                        row_index = row_index + 1
                        worksheet.set_row(row_index,row_min_height)
                        row_index = row_index + 1
                        row_index_end = row_index
                        worksheet.set_row(row_index,row_max_height)

                        # 指标上一行 上部线
                        # grid_table_measure_top_line_format = workbook.add_format({'top': 1,'top_color':'#fd1d1d'})
                        # worksheet.write_blank(row_index_start, 5, '', grid_table_measure_top_line_format)
                        # worksheet.write_blank(row_index_start, 6, '', grid_table_measure_top_line_format)
                        # worksheet.write_blank(row_index_start, 7, '', grid_table_measure_top_line_format)
                        # worksheet.write_blank(row_index_start, 8, '', grid_table_measure_top_line_format)
                        # grid_table_measure_top_right_line_format = workbook.add_format({'top': 1,'top_color':'#fd1d1d','right': 1,'right_color':'#fd1d1d'})
                        # worksheet.write_blank(row_index_start, 9, '', grid_table_measure_top_right_line_format)

                        # 指标
                        grid_table_measure = measure.name
                        grid_table_measure_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':14,'text_wrap':True,'top': 1,'top_color':'#fd1d1d','bottom': 1,'bottom_color':'#fd1d1d','right': 1,'right_color':'#fd1d1d'})
                        worksheet.merge_range(row_index_start, 5, row_index_end, 9, grid_table_measure, grid_table_measure_format)

                        # 指标下一行 最后一格 下部线
                        # grid_table_measure_bottom_right_line_format = workbook.add_format({'bottom': 1,'bottom_color':'#fd1d1d','right': 1,'right_color':'#fd1d1d'})
                        # worksheet.write_blank(row_index_end, 9, '', grid_table_measure_bottom_right_line_format)

                        col_index = 9
                        for i in range(10):
                            # 分值
                            col_index = col_index+2
                            grid_table_score = '['+str(10-i)+']'
                            grid_table_score_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':10,'font_color':'#db1b1b'})
                            worksheet.write(row_index_start + 2, col_index, grid_table_score, grid_table_score_format)

                            # 上部线
                            grid_table_score_line_format = workbook.add_format({'top': 1,'top_color':'#fd1d1d'})
                            worksheet.write_blank(row_index_start, col_index-1, '', grid_table_score_line_format)
                            worksheet.write_blank(row_index_start, col_index+0, '', grid_table_score_line_format)
                            worksheet.write_blank(row_index_start, col_index+1, '', grid_table_score_line_format)

                            if i==9:
                                # 第一行 上侧 右侧 线
                                grid_table_score_top_right_line_format = workbook.add_format({'top': 1,'top_color':'#fd1d1d','right': 2,'right_color':'#fd1d1d'})
                                # 其他行 右侧 线
                                grid_table_score_right_line_format = workbook.add_format({'right': 2,'right_color':'#fd1d1d'})
                                worksheet.write_blank(row_index_start+0, col_index+1, '', grid_table_score_top_right_line_format)
                                worksheet.write_blank(row_index_start+1, col_index+1, '', grid_table_score_right_line_format)
                                worksheet.write_blank(row_index_start+2, col_index+1, '', grid_table_score_right_line_format)
                                worksheet.write_blank(row_index_start+3, col_index+1, '', grid_table_score_right_line_format)
                                worksheet.write_blank(row_index_start+4, col_index+1, '', grid_table_score_right_line_format)

                        # 分值右侧标识块
                        col_index = col_index + 2 + 1
                        grid_table_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                        worksheet.write_blank(row_index_start + 2, col_index, '', grid_table_block_format)

                    content_index_end = row_index

                    # 内容
                    grid_table_content = content.content
                    if(len(content.content)%2==0):
                        position = len(content.content)/2
                        grid_table_content = content.content[0:position] + '\n' + content.content[position:]
                    else:
                        position = int(len(content.content)/2) + 1
                        grid_table_content = content.content[0:position] + '\n' + content.content[position:]
                    grid_table_content_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':14,'text_wrap':True,'left':2,'left_color':'#fd1d1d','right':1,'right_color':'#fd1d1d','top':1,'top_color':'#fd1d1d'})
                    if ci == len(current_contents)-1:
                        grid_table_content_format.set_bottom(2)
                        grid_table_content_format.set_border_color('#fd1d1d')
                    worksheet.merge_range(content_index_start, 1, content_index_end, 4, grid_table_content, grid_table_content_format)

                # 49行 空白
                row_index = row_index + 1
                worksheet.set_row(row_index,row_min_height)

                for i in range(col_index-1):
                    if i==0:
                        continue
                    grid_table_bottom_line_format = workbook.add_format({'top': 2,'top_color':'#fd1d1d'})
                    worksheet.write_blank(row_index, i, '', grid_table_bottom_line_format)

                # 50-53 1-30 说明
                row_index = row_index + 1
                worksheet.set_row(row_index,row_max_height)
                row_index = row_index + 1
                worksheet.set_row(row_index,row_max_height)
                row_index = row_index + 1
                worksheet.set_row(row_index,row_max_height)
                row_index = row_index + 1
                worksheet.set_row(row_index,row_max_height)

                explain = u"注：1、10-9分为优秀，8-7分为良好，6-5分为一般，4分及以下为较差。\n    2、请使用签字笔在对应[ ]内涂满“▇”,以下为错误填涂:[▄]、[〓]、[√]、[●]。\n    3、[ ]为单选框，多涂或漏涂均无效；本表请勿折叠，下方填涂区请勿填涂。"
                explain_format = workbook.add_format({'align':'left','valign':'vcenter','font_size':10,'text_wrap':True})
                worksheet.merge_range(row_index-3, 1, row_index, 30, explain, explain_format)
                                                                                                            
                explain_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                worksheet.write_blank(row_index - 3, 30+2, '', explain_block_format)																						

                # 54行 空白
                row_index = row_index + 1
                worksheet.set_row(row_index,row_min_height)
                # 55行 分值 [空值空值空值空值空值空值空值空值空值空值]
                row_index = row_index + 1
                worksheet.set_row(row_index,row_max_height)

                col_index = 9
                for i in range(10):
                    col_index = col_index+2
                    flag_score = '['+str(10-i)+']'
                    flag_score_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':10,'font_color':'#db1b1b'})
                    worksheet.write(row_index, col_index, flag_score, flag_score_format)

                flag_score_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                worksheet.write_blank(row_index, 30+2, '', flag_score_block_format)

                # 56行 空白
                row_index = row_index + 1
                worksheet.set_row(row_index,row_min_height)
                
                # 57行 标识块
                row_index = row_index + 1
                worksheet.set_row(row_index,row_max_height)

                flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                worksheet.write_blank(row_index, 7, '', flag_block_format)

                col_index = 11
                if entity.name == u'A票':
                    col_index = 11
                if entity.name == u'B票':
                    col_index = 13
                if entity.name == u'C票':
                    col_index = 15
                if entity.name == u'D票':
                    col_index = 17
                if entity.name == u'E票':
                    col_index = 19

                flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                worksheet.write_blank(row_index, col_index, '', flag_block_format)

                flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                worksheet.write_blank(row_index, 30+2, '', flag_score_block_format)

                # 58行 空白
                row_index = row_index + 1
                worksheet.set_row(row_index,row_min_height)
                # 59行 坐标块 [空块空块....]
                row_index = row_index + 1
                worksheet.set_row(row_index,row_max_height)

                for i in range(33):
                    if (i % 2 != 0 or i == 32) and i != 31:
                        flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                        worksheet.write_blank(row_index, i, '', flag_block_format)

                for i in range(100):
                    if i == 31 or i == 30:
                        worksheet.set_column(i, i, col_min_width)
                    elif i == 32:
                        worksheet.set_column(i, i, col_max_width)
                    else:	
                        if i % 2 == 0:
                            worksheet.set_column(i, i, col_min_width)
                        else:
                            worksheet.set_column(i, i, col_max_width)

            workbook.close()

        elif exam.name == u'中层干部年度综合考评':

            page_size = 4
            page_count = len(managers) / page_size + (0 if len(managers) % page_size == 0 else 1)

            for page_no in range(page_count):

                page_start = page_no * page_size
                page_end = page_no * page_size + page_size
                current_managers = managers[page_start:page_end]

                workbook = xlsxwriter.Workbook(os.path.join(org_datetime_path, u'人员'+'_'+str(page_no+1)+'.xlsx'))

                row_min_height = 4
                row_max_height = 11
                row_title_height = 18
                row_subtitle_height = 14

                row_index = 0

                col_min_width = 0.7
                col_max_width = 2.0

                col_index = 0

                for entity in entities:
                    worksheet = workbook.add_worksheet(u'人员'+'_'+entity.name)

                    # 0行 空白
                    row_index = 0
                    col_index = 0
                    worksheet.set_row(row_index,row_min_height)

                    # 1行 1-78列 标题 中层干部年度综合考核评价表（x票）
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_title_height)

                    title = u'中层干部年度综合考核评价表' + ' ' + u'（' + entity.name + u'）'
                    title_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':18})
                    worksheet.merge_range(row_index, 1, row_index, 42, title, title_format)

                    # 2行 空白
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_min_height)

                    # 3行 1-20列 单位  21-30 日期
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_subtitle_height)

                    org_title = u'单位名称：' + org.short_name
                    org_format = workbook.add_format({'align':'left','valign':'vcenter','font_size':11})
                    worksheet.merge_range(row_index, 1, row_index, 25, org_title, org_format)

                    datetime_title = u'考评年度：' + datetimestr
                    datetime_format = workbook.add_format({'align':'right','valign':'vcenter','font_size':11})
                    worksheet.merge_range(row_index, 26, row_index, 42, datetime_title, datetime_format)

                    # 4行 空白
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_min_height)
                                                                                                                
                    # 5-7行 表格标题 [大小大] 1-2 考评内容 3-6 考评指标 7-15,16-24,25-33,34-42,43-51,52-60,61-69,70-78 [小大...]
                    row_index = row_index + 1
                    row_index_start = row_index
                    worksheet.set_row(row_index,row_max_height)
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_min_height)
                    row_index = row_index + 1
                    row_index_end = row_index
                    worksheet.set_row(row_index,row_max_height)
            
                    grid_title_content = u"      姓名  \n考评内容"
                    grid_title_content_format = workbook.add_format({'align':'left','valign':'vcenter','font_size':10,'text_wrap':True,'diag_type':2,'diag_border':1,'diag_color':'#fd1d1d','left':2,'left_color':'#fd1d1d','top':2,'top_color':'#fd1d1d','bottom':2,'bottom_color':'#fd1d1d'})
                    worksheet.merge_range(row_index_start, 1, row_index_end, 6, grid_title_content, grid_title_content_format)

                    grid_table_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                    worksheet.write_blank(row_index_start + 0, 44, '', grid_table_block_format)
                    worksheet.write_blank(row_index_start + 2, 44, '', grid_table_block_format)

                    for mi in range(4):
                        manager = None
                        if mi < len(current_managers):
                            manager = current_managers[mi]
                        col_index = 7 + 9 * mi
                        col_index_start = col_index
                        col_index_end = col_index_start + 8
                        grid_title_manager = manager.name if manager != None else ''
                        grid_title_manager_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':12,'text_wrap':True,'left':1,'left_color':'#fd1d1d','top':2,'top_color':'#fd1d1d','bottom':2,'bottom_color':'#fd1d1d'})
                        if mi == 0:
                            grid_title_manager_format.set_left(2)
                        if mi == 3:
                            grid_title_manager_format.set_right(2)
                            grid_title_manager_format.set_right_color('#fd1d1d')
                        worksheet.merge_range(row_index_start, col_index_start, row_index_end, col_index_end, grid_title_manager, grid_title_manager_format)

                    # 8-N 表格内容

                    current_contents = filter(lambda c: c.exam_id==exam.id,contents)
                    for ci,content in enumerate(current_contents):
                        
                        content_index_start = row_index + 1

                        current_measures = filter(lambda m: m.exam_content_id==content.id,measures)
                        for mmi,measure in enumerate(current_measures):
                            # 8-15行 [小大小大小] 考评内容 1-2[小大] 指标 3-6[小大小大] 考评指标 7-15,16-24,25-33,34-42,43-51,52-60,61-69,70-78 [小大...]
                            row_index = row_index + 1
                            row_index_start = row_index
                            worksheet.set_row(row_index,row_min_height)
                            row_index = row_index + 1
                            worksheet.set_row(row_index,row_max_height)
                            row_index = row_index + 1
                            worksheet.set_row(row_index,row_min_height)
                            row_index = row_index + 1
                            worksheet.set_row(row_index,row_max_height)
                            row_index = row_index + 1
                            worksheet.set_row(row_index,row_min_height)
                            row_index = row_index + 1
                            worksheet.set_row(row_index,row_max_height)
                            row_index = row_index + 1
                            row_index_end = row_index
                            worksheet.set_row(row_index,row_min_height)

                            # 指标
                            grid_table_measure = ''
                            if(len(measure.name)%2==0):
                                position = len(measure.name)/2
                                grid_table_measure = measure.name[0:position] + '\n' + measure.name[position:]
                            else:
                                position = int(len(measure.name)/2) + 1
                                grid_table_measure = measure.name[0:position] + '\n' + measure.name[position:]

                            grid_table_measure_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':11,'text_wrap':True,'right':2,'right_color':'#fd1d1d','top':1,'top_color':'#fd1d1d'})
                            if mmi == 0 and ci == 0:
                                grid_table_measure_format.set_top(2)
                            worksheet.merge_range(row_index_start, 3, row_index_end, 6, grid_table_measure, grid_table_measure_format)

                            col_index = 6

                            # 列
                            for mi in range(4):

                                col_index = col_index + 1
                                
                                # 分值
                                for i in range(4):
                                    
                                    # 分值 7-15,16-24,25-33,34-42,43-51,52-60,61-69,70-78

                                    col_index = col_index + 1

                                    if i == 0 or i == 3:
                                        grid_table_score = '['+str(10-(0 if i==0 else 1))+']'
                                        grid_table_score_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':10,'font_color':'#db1b1b'})
                                        worksheet.write(row_index_start + 1, col_index, grid_table_score, grid_table_score_format)

                                    grid_table_score = '['+str(8-i)+']'
                                    grid_table_score_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':10,'font_color':'#db1b1b'})
                                    worksheet.write(row_index_start + 3, col_index, grid_table_score, grid_table_score_format)

                                    grid_table_score = '['+str(4-i)+']'
                                    grid_table_score_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':10,'font_color':'#db1b1b'})
                                    worksheet.write(row_index_start + 5, col_index, grid_table_score, grid_table_score_format)

                                    col_index = col_index + 1

                                    # 下部线
                                    grid_table_score_line_format = workbook.add_format({'bottom': 1,'bottom_color':'#fd1d1d'})
                                    worksheet.write_blank(row_index_end, col_index-2, '', grid_table_score_line_format)
                                    worksheet.write_blank(row_index_end, col_index-1, '', grid_table_score_line_format)
                                    worksheet.write_blank(row_index_end, col_index+0, '', grid_table_score_line_format)

                                grid_table_score_right_line_format = workbook.add_format({'right': 1,'right_color':'#fd1d1d'})
                                if mi==3:
                                    grid_table_score_right_line_format.set_right(2)
                                worksheet.write_blank(row_index_start+0, col_index, '', grid_table_score_right_line_format)
                                worksheet.write_blank(row_index_start+1, col_index, '', grid_table_score_right_line_format)
                                worksheet.write_blank(row_index_start+2, col_index, '', grid_table_score_right_line_format)
                                worksheet.write_blank(row_index_start+3, col_index, '', grid_table_score_right_line_format)
                                worksheet.write_blank(row_index_start+4, col_index, '', grid_table_score_right_line_format)
                                worksheet.write_blank(row_index_start+5, col_index, '', grid_table_score_right_line_format)

                                grid_table_score_right_bottom_line_format = workbook.add_format({'right':1,'right_color':'#fd1d1d','bottom':1,'bottom_color':'#fd1d1d'})
                                if mi==3:
                                    grid_table_score_right_bottom_line_format.set_right(2)
                                worksheet.write_blank(row_index_start+6, col_index, '', grid_table_score_right_bottom_line_format)

                            # 分值右侧标识块
                            col_index = col_index + 2
                            grid_table_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                            worksheet.write_blank(row_index_start + 1, col_index, '', grid_table_block_format)
                            worksheet.write_blank(row_index_start + 3, col_index, '', grid_table_block_format)
                            worksheet.write_blank(row_index_start + 5, col_index, '', grid_table_block_format)

                        content_index_end = row_index

                        # 内容
                        grid_table_content = ''
                        for t in range(len(content.content)):
                            grid_table_content = grid_table_content + content.content[t:t+1]
                            if t < len(content.content)-1:
                                grid_table_content = grid_table_content + '\n'
                        grid_table_content_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':12,'text_wrap':True,'left':2,'left_color':'#fd1d1d','right':1,'right_color':'#fd1d1d','top':1,'top_color':'#fd1d1d'})
                        
                        if ci == len(current_contents)-1:
                            grid_table_content_format.set_bottom(2)
                            grid_table_content_format.set_border_color('#fd1d1d')
                        worksheet.merge_range(content_index_start, 1, content_index_end, 2, grid_table_content, grid_table_content_format)

                    # 49行 空白
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_min_height)

                    for i in range(col_index - 1):
                        if i==0:
                            continue
                        grid_table_bottom_line_format = workbook.add_format({'top': 2,'top_color':'#fd1d1d'})
                        worksheet.write_blank(row_index, i, '', grid_table_bottom_line_format)

                    # 说明
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_max_height-1)
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_min_height-1)
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_max_height-1)

                    explain = u"注：1、请使用签字笔在对应[ ]内涂满“▇”,以下为错误填涂:[▄]、[〓]、[√]、[●]；\n       2、[ ]为单选框，多涂或漏涂均无效；本表请勿折叠，下方填涂区请勿填涂。"
                    explain_format = workbook.add_format({'align':'left','valign':'vcenter','font_size':10,'text_wrap':True})
                    worksheet.merge_range(row_index-2, 1, row_index, 42, explain, explain_format)
                                                                                                                
                    # 54行 空白
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_min_height)

                    # 55行 分值 [空值空值空值空值空值空值空值空值空值空值] 52-60,61-69,70-78
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_max_height)

                    col_index = 17
                    for i in range(12):
                        flag_score = '['+str(12-i)+']'
                        flag_score_format = workbook.add_format({'align':'center','valign':'vcenter','font_size':10,'font_color':'#db1b1b'})
                        worksheet.write(row_index, col_index, flag_score, flag_score_format)
                        col_index = col_index + 2
                        if ((col_index-7) % 9) % 2 == 0:
                            col_index = col_index + 1

                    flag_score_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                    worksheet.write_blank(row_index, 42+2, '', flag_score_block_format)

                    # # 56行 空白
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_min_height)

                    # # 57行 标识块 2 6 10 77 80
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_max_height)

                    flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                    worksheet.write_blank(row_index, 2, '', flag_block_format)
                    
                    flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                    worksheet.write_blank(row_index, 6, '', flag_block_format)

                    flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                    worksheet.write_blank(row_index, 10, '', flag_block_format)

                    flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                    worksheet.write_blank(row_index, 41, '', flag_block_format)

                    flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                    worksheet.write_blank(row_index, 44, '', flag_block_format)

                    col_index = 12
                    if entity.name == u'A票':
                        col_index = 14
                    if entity.name == u'B票':
                        col_index = 17
                    if entity.name == u'C票':
                        col_index = 19
                    if entity.name == u'D票':
                        col_index = 21
                    if entity.name == u'E票':
                        col_index = 23

                    flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                    worksheet.write_blank(row_index, col_index, '', flag_block_format)

                    # add by yelong 增加人员考评票的页数，用于人员的识别
                    if page_no == 0:
                        col_index = 26
                    if page_no == 1:
                        col_index = 28
                    if page_no == 2:
                        col_index = 30
                    if page_no == 3:
                        col_index = 32
                    if page_no == 4:
                        col_index = 35
                    if page_no == 5:
                        col_index = 37
                    if page_no == 6:
                        col_index = 39
                    if col_index > 25:
                        worksheet.write_blank(row_index, col_index, '', flag_block_format)

                    # # 58行 空白
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_min_height)

                    # # 59行 坐标块 [空块空块....] # 7-15,16-24,25-33,34-42,43-51,52-60,61-69,70-78
                    row_index = row_index + 1
                    worksheet.set_row(row_index,row_max_height)

                    for i in range(45):
                        if i == 0 or i == 1:
                            worksheet.set_column(i, i, col_min_width)
                        elif i == 2:
                            worksheet.set_column(i, i, col_max_width)

                            flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                            worksheet.write_blank(row_index, i, '', flag_block_format)
                        elif i == 79:
                            worksheet.set_column(i, i, col_max_width/2)
                        elif i == 80:
                            worksheet.set_column(i, i, col_max_width)

                            flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                            worksheet.write_blank(row_index, i, '', flag_block_format)
                        elif i >= 7:
                            if ((i-7) % 9) % 2 == 0:
                                worksheet.set_column(i, i, col_min_width)
                            elif ((i-7) % 9) % 2 == 1:
                                worksheet.set_column(i, i, col_max_width)

                                flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                                worksheet.write_blank(row_index, i, '', flag_block_format)
                        elif i % 2 == 0:
                            worksheet.set_column(i, i, col_max_width)

                            flag_block_format = workbook.add_format({'align':'center','valign':'vcenter','fg_color':'#000000'})
                            worksheet.write_blank(row_index, i, '', flag_block_format)
                        elif i % 2 != 0:
                            worksheet.set_column(i, i, col_min_width)

                workbook.close()

def gen_org(org_path,orgs):
    workbook = xlsxwriter.Workbook(org_path)
    worksheet = workbook.add_worksheet()

    row_index = 0

    worksheet.set_row(0,20)

    worksheet.set_column(0, 0, 20)
    worksheet.write(0, 0, u'单位类型', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 1, 60)
    worksheet.write(0, 1, u'单位简称', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 2, 60)
    worksheet.write(0, 2, u'单位全称', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 3, 20)
    worksheet.write(0, 3, u'显示顺序', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    for index,org in enumerate(orgs):

        col_index = 0
        row_index = index + 1

        worksheet.set_row(row_index,20)

        for i in range(4):

            col_index = i
        
            if col_index == 0:
                worksheet.set_column(row_index, col_index, 20)
                worksheet.write(row_index, col_index, org.org_type.name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
            elif col_index == 1:
                worksheet.set_column(row_index, col_index, 60)
                worksheet.write(row_index, col_index, org.short_name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
            elif col_index == 2:
                worksheet.set_column(row_index, col_index, 60)
                worksheet.write(row_index, col_index, org.full_name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
            elif col_index == 3:
                worksheet.set_column(row_index, col_index, 20)
                worksheet.write(row_index, col_index, org.sort, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

    workbook.close()

def gen_manager(org_path,managers):
    workbook = xlsxwriter.Workbook(org_path)
    worksheet = workbook.add_worksheet()

    row_index = 0

    worksheet.set_row(0,20)

    worksheet.set_column(0, 0, 30)
    worksheet.write(0, 0, u'单位', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 1, 15)
    worksheet.write(0, 1, u'姓名', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 2, 15)
    worksheet.write(0, 2, u'人员类型', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 3, 100)
    worksheet.write(0, 3, u'职务', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    worksheet.set_column(0, 4, 15)
    worksheet.write(0, 4, u'显示顺序', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    for index,manager in enumerate(managers):

        col_index = 0
        row_index = index + 1

        worksheet.set_row(row_index,20)

        for i in range(5):
        #for i in range(4):

            col_index = i
        
            if col_index == 0:
                worksheet.set_column(row_index, col_index, 30)
                worksheet.write(row_index, col_index, manager.org.short_name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
            elif col_index == 1:
                worksheet.set_column(row_index, col_index, 15)
                worksheet.write(row_index, col_index, manager.name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
            elif col_index == 2:
                worksheet.set_column(row_index, col_index, 15)
                worksheet.write(row_index, col_index, manager.manager_type.name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
            elif col_index == 3:
                worksheet.set_column(row_index, col_index, 100)
                worksheet.write(row_index, col_index, manager.title, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
            elif col_index == 4:
                worksheet.set_column(row_index, col_index, 15)
                worksheet.write(row_index, col_index, manager.sort, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

    workbook.close()

def gen_result_org(path,year,org_id,exam_entity_id,orgs,exam_entitys,exam_contents,exam_measures,exam_result_teams):
    
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    row_index = 0

    worksheet.set_row(0,20)

    worksheet.set_column(0, 0, 20)
    worksheet.write(0, 0, u'序号', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 1, 30)
    worksheet.write(0, 1, u'单位', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 2, 20)
    worksheet.write(0, 2, u'年份', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 3, 20)
    worksheet.write(0, 3, u'测评主体', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    measure_index = 4
    for measure in exam_measures:
        if measure.exam_content.exam_id == 1 and measure.show == 1:
            worksheet.set_column(0, measure_index, 20)
            worksheet.write(0, measure_index, measure.name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
            measure_index = measure_index + 1

    results = []
    for exam_result_team in exam_result_teams:
        found = False
        for result in results:
            if(exam_result_team.org_id==result['org_id'] and exam_result_team.year==result['year'] and exam_result_team.image_path==result['image_path'] and exam_result_team.exam_entity_id==result['exam_entity_id']):
                found = True
                result['score'][exam_result_team.exam_measure_id] = {
                    "exam_measure_id":exam_result_team.exam_measure_id,
                    "exam_measure":exam_result_team.exam_measure,
                    "score":exam_result_team.score
                }
        if not found:
            result = {
                'image_path':exam_result_team.image_path,
                'exam_entity':exam_result_team.exam_entity,
                'exam_entity_id':exam_result_team.exam_entity_id,
                'org':exam_result_team.org,
                'org_id':exam_result_team.org_id,
                'validity':exam_result_team.validity,
                'year':exam_result_team.year,
                'score':{
                }
            }
            result['score'][exam_result_team.exam_measure_id] = {
                "exam_measure_id":exam_result_team.exam_measure_id,
                "exam_measure":exam_result_team.exam_measure,
                "score":exam_result_team.score
            }
            results.append(result)

    row_index = 1
    result_index = 1
    for result in results:
        col_index = 0
    
        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, str(result_index), workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, result['org'].short_name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, result['year'], workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, result['exam_entity'].name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        for measure in exam_measures:
            if measure.exam_content.exam_id == 1 and measure.show == 1:

                score = result['score'][measure.id]

                worksheet.set_column(row_index, col_index, 20)
                worksheet.write(row_index, col_index, score['score'], workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
                
                col_index = col_index + 1

        row_index = row_index + 1
        result_index = result_index + 1

    workbook.close()

def gen_result_manager(path,year,manager_id,exam_entity_id,orgs,exam_entitys,exam_contents,exam_measures,exam_result_teams,managers,exam_result_managers):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet()

    row_index = 0

    worksheet.set_row(0,20)

    worksheet.set_column(0, 0, 20)
    worksheet.write(0, 0, u'序号', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 1, 30)
    worksheet.write(0, 1, u'单位', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 2, 20)
    worksheet.write(0, 2, u'年份', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 3, 20)
    worksheet.write(0, 2, u'姓名', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 4, 20)
    worksheet.write(0, 3, u'测评主体', workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    measure_index = 5
    for measure in exam_measures:
        if measure.exam_content.exam_id == 2 and measure.show == 1:
            worksheet.set_column(0, measure_index, 20)
            worksheet.write(0, measure_index, measure.name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
            measure_index = measure_index + 1

    results = []
    for exam_result_manager in exam_result_managers:
        found = False
        for result in results:
            if(exam_result_manager.manager_id==result['manager_id'] and exam_result_manager.year==result['year'] and exam_result_manager.image_path==result['image_path'] and exam_result_manager.exam_entity_id==result['exam_entity_id']):
                found = True
                result['score'][exam_result_manager.exam_measure_id] = {
                    "exam_measure_id":exam_result_manager.exam_measure_id,
                    "exam_measure":exam_result_manager.exam_measure,
                    "score":exam_result_manager.score
                }
        if not found:
            result = {
                'image_path':exam_result_manager.image_path,
                'exam_entity':exam_result_manager.exam_entity,
                'exam_entity_id':exam_result_manager.exam_entity_id,
                'manager':exam_result_manager.manager,
                'manager_id':exam_result_manager.manager_id,
                'validity':exam_result_manager.validity,
                'year':exam_result_manager.year,
                'score':{
                }
            }
            result['score'][exam_result_manager.exam_measure_id] = {
                "exam_measure_id":exam_result_manager.exam_measure_id,
                "exam_measure":exam_result_manager.exam_measure,
                "score":exam_result_manager.score
            }
            results.append(result)

    row_index = 1
    result_index = 1
    for result in results:
        col_index = 0

        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, str(result_index), workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, result['manager'].org.short_name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, result['year'], workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, result['manager'].name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        worksheet.set_column(row_index, col_index, 20)
        worksheet.write(row_index, col_index, result['exam_entity'].name, workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))

        col_index = col_index + 1

        for measure in exam_measures:
            if measure.exam_content.exam_id == 2 and measure.show == 1:

                score = result['score'][measure.id]

                worksheet.set_column(row_index, col_index, 20)
                worksheet.write(row_index, col_index, score['score'], workbook.add_format({'align':'left','valign':'vcenter','font_size':16,'font_color':'#000000'}))
                
                col_index = col_index + 1

        row_index = row_index + 1
        result_index = result_index + 1

    workbook.close()

def gen_report_manager(report_path,year,exams,measures,contents):
    workbook = xlsxwriter.Workbook(report_path)
    worksheet = workbook.add_worksheet()

    worksheet.set_row(0,20)
    worksheet.set_row(1,20)
    worksheet.set_row(2,20)

    worksheet.set_column(0, 0, 15)
    worksheet.merge_range(0, 0, 2, 0, u'序号', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 1, 30)
    worksheet.merge_range(0, 1, 2, 1, u'单位', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 2, 30)
    worksheet.merge_range(0, 2, 2, 2, u'姓名', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 3, 30)
    worksheet.merge_range(0, 3, 2, 3, u'职务', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    worksheet.set_column(0, 4, 20)
    worksheet.merge_range(0, 4, 0, 5, u'汇总得分', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    worksheet.set_column(0, 4, 20)
    worksheet.merge_range(1, 4, 2, 4, u'得分', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    worksheet.set_column(0, 5, 20)
    worksheet.merge_range(1, 5, 2, 5, u'排名', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    worksheet.set_column(0, 6, 20)
    worksheet.merge_range(0, 6, 2, 6, u'部门业绩得分', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    # worksheet.set_column(0, 6, 20)
    # worksheet.merge_range(1, 6, 2, 6, u'得分', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    # worksheet.set_column(0, 7, 20)
    # worksheet.merge_range(1, 7, 2, 7, u'排名', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))


    # worksheet.set_column(0, 8, 20)
    # worksheet.set_column(0, 9, 20)

    worksheet.merge_range(1, 7, 2, 7, u'合计', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    # worksheet.write(2, 8, u'得分', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    # worksheet.write(2, 9, u'排名', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    row_index = 1
    col_index = 8

    measure_all_count = 0

    for content in contents:

        if content.show == 0:
            continue

        print content.content

        measure_count = 1

        worksheet.set_column(0, col_index+measure_count-1, 15)

        worksheet.write(2, col_index+measure_count-1, u'小计', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

        for measure in measures:

            if measure.exam_content.id == content.id:
                print measure.name

                measure_count = measure_count + 1

                measure_all_count = measure_all_count + 1

                worksheet.set_column(0, col_index+measure_count-1, 15)
                worksheet.write(2, col_index+measure_count-1, measure.name, workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

        worksheet.merge_range(1, col_index, 1, col_index+measure_count-1, content.content, workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

        col_index = col_index + measure_count

    worksheet.merge_range(0, 7, 0, 7+measure_all_count+2+1, u'民主测评', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    row_index = 2
    col_index = 0

    for index,exam in enumerate(exams):

        row_index = row_index+1
        col_index = 0

        worksheet.write(row_index, 0, index+1, workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, 1, exam['org_name'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, 2, exam['manager_name'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, 3, exam['title'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))

        worksheet.write(row_index, 4, exam['manager_sum_score'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, 5, exam['manager_sum_sort'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, 6, exam['org_score'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        # worksheet.write(row_index, 7, exam['org_sort'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, 7, exam['manager_score'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        # worksheet.write(row_index, 9, exam['manager_sort'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        col_index = 8

        for content in contents:

            if content.show == 0:
                continue

            measure_count = 1

            text = exam['content_score_'+str(content.id)]

            worksheet.write(row_index, col_index+measure_count-1, text, workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))

            for measure in measures:
                
                if measure.exam_content.id == content.id:
                    print measure.name
                    
                    text = exam['measure_score_'+str(measure.id)]

                    measure_count = measure_count + 1

                    worksheet.write(row_index, col_index+measure_count-1, text, workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
            col_index = col_index + measure_count

    workbook.close()

def gen_report_team(report_path,year,exams,measures,contents):
    workbook = xlsxwriter.Workbook(report_path)
    worksheet = workbook.add_worksheet()

    worksheet.set_row(0,20)
    worksheet.set_row(1,20)

    worksheet.set_column(0, 0, 8)
    worksheet.merge_range(0, 0, 1, 0, u'序号', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 1, 25)
    worksheet.merge_range(0, 1, 1, 1, u'单位', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 2, 15)
    worksheet.merge_range(0, 2, 1, 2, u'汇总得分', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    worksheet.set_column(0, 3, 8)
    worksheet.merge_range(0, 3, 1, 3, u'排名', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    worksheet.set_column(0, 4, 15)
    worksheet.merge_range(0, 4, 1, 4, u'企业党建', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 5, 15)
    worksheet.merge_range(0, 5, 1, 5, u'班子业绩', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))
    
    worksheet.set_column(0, 6, 15)
    worksheet.merge_range(0, 6, 1, 6, u'民主测评', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

    row_index = 0
    col_index = 7

    for content in contents:

        if content.show == 0:
            continue

        print content.content

        measure_count = 1
        
        worksheet.set_column(0, col_index+measure_count-1, 15)

        worksheet.write(1, col_index+measure_count-1, u'小计', workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

        for measure in measures:

            if measure.exam_content.id == content.id:
                print measure.name

                measure_count = measure_count + 1

                worksheet.set_column(0, col_index+measure_count-1, 15)
                worksheet.write(1, col_index+measure_count-1, measure.name, workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

        worksheet.merge_range(0, col_index, 0, col_index+measure_count-1, content.content, workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#DDDDDD'}))

        col_index = col_index + measure_count

    row_index = 1
    col_index = 0

    for index,exam in enumerate(exams):

        row_index = row_index+1
        col_index = 0

        worksheet.write(row_index, col_index+0, index+1, workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, col_index+1, exam['org_name'], workbook.add_format({'align':'center','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, col_index+2, exam['org_sum_score'], workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        worksheet.write(row_index, col_index+3, exam['org_sum_sort'], workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))

        worksheet.write(row_index, col_index+4, exam['dj_score'], workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))

        worksheet.write(row_index, col_index+5, exam['yj_score'], workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))

        worksheet.write(row_index, col_index+6, exam['org_score'], workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
        col_index = 7

        for content in contents:

            if content.show == 0:
                continue

            measure_count = 1

            text = exam['content_score_'+str(content.id)]

            worksheet.write(row_index, col_index+measure_count-1, text, workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))

            for measure in measures:
                
                if measure.exam_content.id == content.id:
                    print measure.name
                    
                    text = exam['measure_score_'+str(measure.id)]

                    measure_count = measure_count + 1

                    worksheet.write(row_index, col_index+measure_count-1, text, workbook.add_format({'align':'right','valign':'vcenter','font_size':16,'font_color':'#000000','fg_color':'#FFFFFF'}))
        
            col_index = col_index + measure_count

    workbook.close()

def main(argv):
    print datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

if __name__ == '__main__':
    main(sys.argv[1:])