/***************************************************************************
 * 
 * Copyright (c) 2013 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/

/**
 * @file Cluster_Kmeans.h
 * @author yaojia(com@baidu.com)
 * @date Tue Aug 13 15:45:58 CST 2013
 * @brief 
 *  K-means工具函数接口及数据结构
 **/

#ifndef  __CLUSTER_KMEANS_H_
#define  __CLUSTER_KMEANS_H_


#include <getopt.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "ml_data.h"
#include "ul_conf.h"
#include "ul_log.h"
#include <pthread.h>
#include <float.h>
#include <math.h>

#define CLUSTER_KMEANS_BUFFER_LEN 10240000
#define CLUSTER_KMEANS_MURMUR_SEED  101
#define CLUSTER_KMEANS_DATA_ID_LEN  1000
#define CLUSTER_KMEANS_MAX_TOKEN_LEN  1000000
#define CLUSTER_KMEANS_MAX_CONF_ITEM 100
#define CLUSTER_KMEANS_PROJECT_NUM 1

//-------------------------------配置文件参数--------------------//
/** 聚类算法名称*/
#define CLUSTER_ALGO "algorithm"  
#define CLUSTER_KMEANS_NAME "kmeans"
/**K-Means聚类主体程序  0-更新 1-训练 2-应用*/
#define CLUSTER_KMEANS_EXE_MODEL "exe_model"
/**K-Means聚类类别*/
#define CLUSTER_KMEANS_K "K"
/**K-Means聚类最大迭代次数*/
#define CLUSTER_KMEANS_MAXITER "max_iter"
/**K-Means聚类迭代最小差异值（两次迭代差异小于此值就stop）*/
#define CLUSTER_KMEANS_EPSILON "epsilon"
/**K-Means聚类中心点初始化方法 1-Random 2-Kmeans++ 3-MinMax*/
#define CLUSTER_KMEANS_INIT_CENTERS "init_centers"
/**K-Means聚类主体程序运行次数*/
#define CLUSTER_KMEANS_ATTEMPTS "attempts"
/**K-Means聚类距离度量方式 1-欧式 2-cos*/
#define CLUSTER_KMEANS_DISMOD "dis_mod"
/**K-Means聚类样例结果是否输出（输出耗时长）*/
#define CLUSTER_KMEANS_OUT_TAG "samples_result_tag"
/**K-Means聚类一次读入内存最大行数*/
#define CLUSTER_KMEANS_MAX_INNERLINES "max_innerlines"
/**K-Means聚类通过max_innerlines读取文件次数*/
#define CLUSTER_KMEANS_READ_TIMES "read_times"
/**K-Means聚类中心点信息输出文件*/
#define CLUSTER_KMEANS_CENTERS_FILE "cluster_centers_file"
/**K-Means聚类样例结果输出文件*/
#define CLUSTER_KMEANS_SAMPLES_FILE "cluster_samples_file"
/**K-Means聚类字典*/
#define CLUSTER_KMEANS_DICT_FILE "cluster_dict_file"
/**K-Means聚类选中迭代数据后迭代次数*/
#define CLUSTER_KMEANS_INNER_ITER "inner_iter"
/**K-Means聚类特征是否进行映射*/
#define CLUSTER_KMEANS_MAP "feature_map"
/**K-Means聚类特征映射区间（可用于降维）*/
#define CLUSTER_KMEANS_MOD_SIZE "MOD_SIZE"
/**K-Means聚类 多线程*/
#define CLUSTER_KMEANS_MULTI_THREAD "multi_thread"
/**K-Means聚类 SAMPLE数据*/
#define CLUSTER_KMEANS_SAMPLE "SAMPLE"

typedef enum {
    KMEANS_RANDOM_CENTERS = 1,      /**< 初始化中心点选择Random */
    KMEANS_PP_CENTERS = 2,          /**< 初始化中心点选择Kmeans++ */
    KMEANS_MM_CENTERS = 3           /**< 初始化中心点选择MinMax */
} INIT_TYPE;

typedef enum{
    KMEANS_EXE_UPDATE = 0,          /**< Kmeans主体程序选择"更新" */
    KMEANS_EXE_TRAIN = 1,           /**< Kmeans主体程序选择"训练" */
    KMEANS_EXE_TEST = 2             /**< Kmeans主体程序选择"应用" */
} EXE_MODEL;

typedef enum {
    EUCLID = 1,                     /**< Kmeans距离度量使用"欧式距离" */
    CONSINE = 2                     /**< Kmeans距离度量使用"cos距离" */
} DISMOD_TYPE;

typedef struct _cluster_kmeans_conf_t {
    EXE_MODEL exe_model;            /**< Kmeans主体程序选择*/
    u_int K;                        /**< Kmeans聚类类别数目*/
    u_int max_iter;                 /**< Kmeans最大迭代次数*/
    float epsilon;                  /**< Kmeans两次主体程序之间最小差异值*/
    INIT_TYPE init_centers;         /**< Kmeans初始中心点选项*/
    u_int attempts;                 /**< Kmeans主体程序运行次数*/
    DISMOD_TYPE dis_mod;            /**< Kmeans距离度量方式*/
    bool samples_result_tag;        /**< Kmeans聚类样例结果信息是否输出选项*/
    u_int max_innerlines;           /**< Kmeans聚类读入内存最大行数*/
    u_int read_times;               /**< Kmeans聚类读入最大行数进内存次数*/
    u_int MOD_SIZE;                 /**< Kmeans特征区间*/
    u_int feature_map;              /**< Kmeans是否进行特征映射选项*/
    char *cluster_centers_file;     /**< Kmeans聚类中心点信息输出文件*/
    char *cluster_samples_file;     /**< Kmeans样例聚类信息输出文件*/
    char *cluster_dict_file;        /**< KNN的dict文件*/
    u_long allsamples_num;          /**< 所有样例数目*/
    u_int thread_num;               /**< 多进程的进程数*/
    u_int inner_iter;               /**< 选中迭代数据后迭代次数*/
    u_int SAMPLE;                   /**< 每轮迭代为每类选中的sample数据量*/
} kmeans_conf_t;

typedef struct _cluster_kmeans_sample_info_t{
    u_long smaple_id;               /**< 样例ID*/
    u_long begin;                   /**< 样例特征所在区间开始位置*/
    u_long end;                     /**< 样例特征所在区间结束位置*/
    double sample_squarednorm;      /**< 样例本身平方和*/
    double dist_center;             /**< 样例到最近中心点距离*/
    u_int member_center_id;         /**< 样例所属中心点ID*/
} sample_info_t;

typedef struct _cluster_kmeans_feature_info_t{
    u_int feature_id;               /**< 特征ID*/
    double value;                   /**< 该特征的VALUE*/
} feature_info_t;

typedef struct _cluster_kmeans_dataset_t{
    feature_info_t *features;       /**< 内存中样例的所有特征*/
    sample_info_t *samples;         /**< 内存中样例*/
    long long features_num;         /**< 内存中样例总的特征数*/
    u_int samples_num;              /**< 放入内存的样例数目*/
    bool *innersamples_tag;         /**< 内存中样例是否继续用于迭代选项*/
    char *allsamples_tag;           /**< 所有样例的状态 /0-未读入内存 1-待读入内存 2-已读入内存*/
    u_long allsamples_num;          /**< 所有样例数目*/
    u_long outsamples_num;          /**< 未读入内存的样例数目*/
} kmeans_dataset_t;

typedef struct _cluster_kmeans_model_t{
    u_int K;                        /**< Kmeans聚类类别数目*/
    double **centers;               /**< Kmeans聚类结果各中心点信息*/
    double *centers_squarednorm;    /**< Kmeans聚类结果各中心点平方和*/
    double *centers_average_dist;   /**< Kmeans聚类各中心点的样例距离平均值*/
    double *max_sample_id;
    double *max_sample_dist;
    u_int *centers_update_num;     /**< Kmeans聚类各中心点更新次数*/
    double *projection_vector;      /**< Kmeans聚类用于投影的向量*/
    double *projection_dist;        /**< Kmeans聚类各中心点向量投影值*/
    int *projection_centers_id;     /**< Kmeans聚类各中心点向量投影值的排序*/
} kmeans_model_t;


typedef struct _mutil_thread_node{
    u_int start;                    /**< 多线程样例的第一个样例号*/
    u_int end;                      /**< 多线程样例的最后一个样例号*/
    kmeans_dataset_t *data;         /**< 多线程所需参数 : 所有内存中样例信息*/
    kmeans_conf_t *conf;            /**< 多线程所需参数 : 配置信息*/
    kmeans_model_t *model;          /**< 多线程所需参数 : 聚类中心点信息*/
} thread_node;

//-----------------------读取配置信息函数------------------------------
/**
 * @brief 输出help信息
 * @param [in] argv[0]
 * no return
 * */
void usage(const char *program_name);
/**
 * @brief 命令行参数读取
 * @param [in] argc,*argv :     命令行参数信息
 * @param [in] conf_fname :     配置文件地址
 * @param [in] samples_fname :  样例信息文件地址
 * @param [in] cluster_conf :   配置文件结构体
 * return int
 *      -1  读取参数失败
 *      1   读取参数成功
 * */
int cluster_parse_args(int argc, char *argv[], char *&conf_fname, char *&samples_fname, kmeans_conf_t *cluster_conf);
/**
 * @brief 命令行参数读取
 * @param [in] conf_fname :     配置文件地址
 * @param [in] conf :           配置文件结构体
 * return int
 *      -1  读取配置文件失败
 *      1   读取配置文件成功
 * */
int cluster_read_conf(const char *conf_fname, kmeans_conf_t *conf);

//-----------------------基础模块函数接口------------------------------
/**
 * @brief 中心点文件信息载入
 * @param [in] model:           聚类模型
 * @param [in] conf :           配置文件结构体
 * return int
 *      -1  载入中心点信息失败
 *      1   载入中心点信息成功
 * */
int centers_load(kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 预处理（剔除不需要使用的样例）
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  预处理失败
 *      1   预处理成功
 * */
int preprocess(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 初始化K个中心点
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  中心点初始化失败
 *      1   中心点初始化成功
 * */
int init_k_centers(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 从硬盘中选择需要进行训练的样例
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * return int
 *      -1  选择样例成功
 *      1   选择样例失败
 * */
int samples_choose(kmeans_dataset_t *data, kmeans_conf_t *conf);
/**
 * @brief 根据samples_choose()从硬盘中载入数据
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] samples_fname :  训练样例信息文件
 * return int
 *      -1  数据载入失败
 *      1   数据载入成功
 * */
int data_load(char *samples_fname, kmeans_dataset_t *data, kmeans_conf_t *conf);
/**
 * @brief 选择继续迭代样例
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * @param [in] left_iter :      还剩迭代次数
 * return int
 *      -1  样例选择失败
 *      1   样例选择成功
 * */
int next_samples_choose(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 为所有样例找到最近邻中心点
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  找最近邻失败
 *      1   找最近邻成功
 * */
int nearest_node(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 更新中心点
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  中心点更新失败
 *      1   中心点更新成功
 * */
int centers_update(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model, double
&max_epilson, u_int &rand_num);
/**
 * @brief 从文件读样例，并找到最近邻中心点
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  失败
 *      1   成功
 * */
int line_to_center(char *samples_fname, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 输出聚类中心点信息
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  失败
 *      1   成功
 * */
int centers_info_out(kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 输出聚类结果样例信息
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  失败
 *      1   成功
 * */
int samples_result(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 初始化一个聚类模型
 * @param [in] conf :           配置文件结构体
 * return kmeans_model_t *
 *      NULL    失败
 *      other   聚类模型指针
 * */
kmeans_model_t *centers_created( kmeans_conf_t *conf);
/**
 * @brief 初始化一个样例数据模型
 * @param [in] conf :           配置文件结构体
 * return kmeans_model_t *
 *      NULL    失败
 *      other   数据模型指针
 * */
kmeans_dataset_t * data_created(kmeans_conf_t *conf);
/**
 * @brief 为用户输入的key找到所属的特征向量
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  失败
 *      1   成功
 * */
int KNN_get_center(kmeans_model_t *model, kmeans_conf_t *conf, kmeans_dataset_t *data);
/**
 * @brief 为用户输入的key的特征向量在字典中找k近邻
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  失败
 *      1   成功
 * */
int KNN_samples_result(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief 释放已占用内存
 * @param [in] data :           聚类样例数据
 * @param [in] conf :           配置文件结构体
 * @param [in] model :          聚类模型
 * return int
 *      -1  失败
 *      1   成功
 * */
int free_strcut(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);


#endif  //__MY_CLUSTER_H_
/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
