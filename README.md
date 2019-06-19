# FreeVolumeComparison
信息比对系统设计
信息来自两个地方，一个是数据库，另一个是网页上显示的前台数据                                                                       
数据库：可以直接通过访问DBlink连接数据库，获取数据，获取的数据用迭代器处理      
网页数据：由于网站设置多种验证方式，因此采用selenium进行爬取数据，用beautifulsoup处理采集的数据                        
菜单：使用python内置GUI tKinter设计一个可以简易操作的界面
最后使用pyinstall 打包                                                    
