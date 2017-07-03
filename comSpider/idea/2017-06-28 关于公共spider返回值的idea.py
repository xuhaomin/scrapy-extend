

思想：
    基于css，xpath建立的dom树，item作为叶子节点进行采集 
    'xpath': （对应xpath方法）
        {
            xpath1: {
                xpath1-2: {
                    '__use':'dump',
                    'name':xpath1-2-1,
                    'sign':xpath1-2-2,
                    'location':xpath1-2-3,
                }, 
            }
        }
   're':（对应re方法）
        {
            '__use':'dump',
            itemX:regex1,
        }
    'css': （对应css方法）
        {
            css1: {
                css1-2: {
                    '__use':'dump',
                    item5:css1-2-1,
                    item6:css1-2-2,
                    item7:css1-2-3,
                }, 
            }
        }


接口返回值目前有两种方案：
方案一 返回包含多个item的list  例如 return [item1,item2,item3]
方案二 是返回单个item，其各字段的值是采集下来对应值的list   例如 return item = {key1:[v1,v2,v3],key2:[v1,v2,v3]}


方案一就是初始化一个list，然后遍历dom树，把所有叶子节点采集到的内容作为一个item加入list中
    那这样，如果item需要不同方法得到，如：
    'xpath': 
        {
            xpath1: {
                xpath1-2: {
                    '__use':'dump',
                    'name':xpath1-2-1,
                    }
                }
        }，
    're':
        {
            '__use':'dump',
            'sign':regex,
        }
    这样 name 和 sign 字段就得分别在不同item中返回  因为它们不在一个叶子节点下。


方案二就是在开始初始化一个item，遍历dom树，把所有叶子节点采集到的值，根据字段名对应的插入初始化建立的item中
    但是同样：
    'xpath': 
        {
            xpath1: {
                xpath1-2: {
                    '__use':'dump',
                    'name':xpath1-2-1,
                    }
                }
        }，
    're':
        {
            '__use':'dump',
            'sign':regex,
        }

    面对这样一个情况，如果name返回了10个值，sign返回了9个值，很难一一对应。


返回单个item如果遇到单个页面，例如列表页，需要返回多个item的情况会比较麻烦。  
    例如：出现某个值缺失，key1采了10个值 key2采了9个值，就比较难匹配，会发生冲突
    解决方法： 写xpath或者回调时，尽量让返回值数量匹配，或者将采集结果丢到item-pipeline进行处理。
返回多个item，面对需要多种（例如正则加xpath）方法取不同字段值的情况，比较麻烦，
    比如key1，key2通过正则取，key3通过xpath取，key4通过某函数取，不同方法产生的值就得写在不同item里（分属于不同叶子结点），后续处理起来比较麻烦，
    解决方法： 尽量只用一种方案取值（只用xpath选择器或者只用函数）

或者写两种spider：
    列表页的信息采集用返回多个item的spider
    详情页的信息采集用返回单个item的spider


想了想，还是返回单个item，最后交给item-pipeline进行处理比较合适
除了item-pipeline，items中还可以定义processor-out方法，来处理取回来的值
返回多个item后续都不知道怎么处理了

先这样吧，有需求以后再说

┐(´～｀；)┌

