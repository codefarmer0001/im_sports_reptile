#!/bin/bash
# -*- coding: utf-8 -*-

# 提示用户输入名字
echo '1、选择获取列表1'
echo '2、选择获取列表2'
echo '3、选择获取列表3'
echo '4、选择获取详情1'
echo '5、选择获取详情2'
echo '6、选择获取详情3'
echo '7、选择获取详情4'
echo '8、选择获取详情5'
echo '9、选择获取详情6'
echo '10、选择获取详情7'
echo '11、选择获取详情8'
echo '12、选择获取详情9'
echo '13、选择获取详情10'


read -p '请输入要执行的程序' NUM

echo $NUM

if [[ "$NUM" == '1' ]]
then
echo '执行MODE为m1'
code=m1
echo $code

elif [[ "$NUM" == '2' ]]
then
echo '执行MODE为m2'
code=m2
echo $code

elif [[ "$NUM" == '3' ]]
then
echo '执行MODE为m3'
code=m3
echo $code

elif [[ "$NUM" == '4' ]]
then
echo '执行MODE为d1'
code=d1
echo $code

elif [[ "$NUM" == '5' ]]
then
echo '执行MODE为d2'
code=d2
echo $code

elif [[ "$NUM" == '6' ]]
then
echo '执行MODE为d3'
code=d3
echo $code

elif [[ "$NUM" == '7' ]]
then
echo '执行MODE为d4'
code=d4
echo $code

elif [[ "$NUM" == '8' ]]
then
echo '执行MODE为d5'
code=d5
echo $code

elif [[ "$NUM" == '9' ]]
then
echo '执行MODE为d9'
code=d6
echo $code

elif [[ "$NUM" == '10' ]]
then
echo '执行MODE为d7'
code=d7
echo $code

elif [[ "$NUM" == '11' ]]
then
echo '执行MODE为d8'
code=d8
echo $code

elif [[ "$NUM" == '12' ]]
then
echo '执行MODE为d9'
code=d9
echo $code

elif [[ "$NUM" == '13' ]]
then
echo '执行MODE为d10'
code=d10
echo $code

fi

export MODE=$code
nohup python3 src/main.py $code > $code.log 2>&1 &
tail -f $code.log