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
 *  K-means���ߺ����ӿڼ����ݽṹ
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

//-------------------------------�����ļ�����--------------------//
/** �����㷨����*/
#define CLUSTER_ALGO "algorithm"  
#define CLUSTER_KMEANS_NAME "kmeans"
/**K-Means�����������  0-���� 1-ѵ�� 2-Ӧ��*/
#define CLUSTER_KMEANS_EXE_MODEL "exe_model"
/**K-Means�������*/
#define CLUSTER_KMEANS_K "K"
/**K-Means��������������*/
#define CLUSTER_KMEANS_MAXITER "max_iter"
/**K-Means���������С����ֵ�����ε�������С�ڴ�ֵ��stop��*/
#define CLUSTER_KMEANS_EPSILON "epsilon"
/**K-Means�������ĵ��ʼ������ 1-Random 2-Kmeans++ 3-MinMax*/
#define CLUSTER_KMEANS_INIT_CENTERS "init_centers"
/**K-Means��������������д���*/
#define CLUSTER_KMEANS_ATTEMPTS "attempts"
/**K-Means������������ʽ 1-ŷʽ 2-cos*/
#define CLUSTER_KMEANS_DISMOD "dis_mod"
/**K-Means������������Ƿ�����������ʱ����*/
#define CLUSTER_KMEANS_OUT_TAG "samples_result_tag"
/**K-Means����һ�ζ����ڴ��������*/
#define CLUSTER_KMEANS_MAX_INNERLINES "max_innerlines"
/**K-Means����ͨ��max_innerlines��ȡ�ļ�����*/
#define CLUSTER_KMEANS_READ_TIMES "read_times"
/**K-Means�������ĵ���Ϣ����ļ�*/
#define CLUSTER_KMEANS_CENTERS_FILE "cluster_centers_file"
/**K-Means���������������ļ�*/
#define CLUSTER_KMEANS_SAMPLES_FILE "cluster_samples_file"
/**K-Means�����ֵ�*/
#define CLUSTER_KMEANS_DICT_FILE "cluster_dict_file"
/**K-Means����ѡ�е������ݺ��������*/
#define CLUSTER_KMEANS_INNER_ITER "inner_iter"
/**K-Means���������Ƿ����ӳ��*/
#define CLUSTER_KMEANS_MAP "feature_map"
/**K-Means��������ӳ�����䣨�����ڽ�ά��*/
#define CLUSTER_KMEANS_MOD_SIZE "MOD_SIZE"
/**K-Means���� ���߳�*/
#define CLUSTER_KMEANS_MULTI_THREAD "multi_thread"
/**K-Means���� SAMPLE����*/
#define CLUSTER_KMEANS_SAMPLE "SAMPLE"

typedef enum {
    KMEANS_RANDOM_CENTERS = 1,      /**< ��ʼ�����ĵ�ѡ��Random */
    KMEANS_PP_CENTERS = 2,          /**< ��ʼ�����ĵ�ѡ��Kmeans++ */
    KMEANS_MM_CENTERS = 3           /**< ��ʼ�����ĵ�ѡ��MinMax */
} INIT_TYPE;

typedef enum{
    KMEANS_EXE_UPDATE = 0,          /**< Kmeans�������ѡ��"����" */
    KMEANS_EXE_TRAIN = 1,           /**< Kmeans�������ѡ��"ѵ��" */
    KMEANS_EXE_TEST = 2             /**< Kmeans�������ѡ��"Ӧ��" */
} EXE_MODEL;

typedef enum {
    EUCLID = 1,                     /**< Kmeans�������ʹ��"ŷʽ����" */
    CONSINE = 2                     /**< Kmeans�������ʹ��"cos����" */
} DISMOD_TYPE;

typedef struct _cluster_kmeans_conf_t {
    EXE_MODEL exe_model;            /**< Kmeans�������ѡ��*/
    u_int K;                        /**< Kmeans���������Ŀ*/
    u_int max_iter;                 /**< Kmeans����������*/
    float epsilon;                  /**< Kmeans�����������֮����С����ֵ*/
    INIT_TYPE init_centers;         /**< Kmeans��ʼ���ĵ�ѡ��*/
    u_int attempts;                 /**< Kmeans����������д���*/
    DISMOD_TYPE dis_mod;            /**< Kmeans���������ʽ*/
    bool samples_result_tag;        /**< Kmeans�������������Ϣ�Ƿ����ѡ��*/
    u_int max_innerlines;           /**< Kmeans��������ڴ��������*/
    u_int read_times;               /**< Kmeans�����������������ڴ����*/
    u_int MOD_SIZE;                 /**< Kmeans��������*/
    u_int feature_map;              /**< Kmeans�Ƿ��������ӳ��ѡ��*/
    char *cluster_centers_file;     /**< Kmeans�������ĵ���Ϣ����ļ�*/
    char *cluster_samples_file;     /**< Kmeans����������Ϣ����ļ�*/
    char *cluster_dict_file;        /**< KNN��dict�ļ�*/
    u_long allsamples_num;          /**< ����������Ŀ*/
    u_int thread_num;               /**< ����̵Ľ�����*/
    u_int inner_iter;               /**< ѡ�е������ݺ��������*/
    u_int SAMPLE;                   /**< ÿ�ֵ���Ϊÿ��ѡ�е�sample������*/
} kmeans_conf_t;

typedef struct _cluster_kmeans_sample_info_t{
    u_long smaple_id;               /**< ����ID*/
    u_long begin;                   /**< ���������������俪ʼλ��*/
    u_long end;                     /**< �������������������λ��*/
    double sample_squarednorm;      /**< ��������ƽ����*/
    double dist_center;             /**< ������������ĵ����*/
    u_int member_center_id;         /**< �����������ĵ�ID*/
} sample_info_t;

typedef struct _cluster_kmeans_feature_info_t{
    u_int feature_id;               /**< ����ID*/
    double value;                   /**< ��������VALUE*/
} feature_info_t;

typedef struct _cluster_kmeans_dataset_t{
    feature_info_t *features;       /**< �ڴ�����������������*/
    sample_info_t *samples;         /**< �ڴ�������*/
    long long features_num;         /**< �ڴ��������ܵ�������*/
    u_int samples_num;              /**< �����ڴ��������Ŀ*/
    bool *innersamples_tag;         /**< �ڴ��������Ƿ�������ڵ���ѡ��*/
    char *allsamples_tag;           /**< ����������״̬ /0-δ�����ڴ� 1-�������ڴ� 2-�Ѷ����ڴ�*/
    u_long allsamples_num;          /**< ����������Ŀ*/
    u_long outsamples_num;          /**< δ�����ڴ��������Ŀ*/
} kmeans_dataset_t;

typedef struct _cluster_kmeans_model_t{
    u_int K;                        /**< Kmeans���������Ŀ*/
    double **centers;               /**< Kmeans�����������ĵ���Ϣ*/
    double *centers_squarednorm;    /**< Kmeans�����������ĵ�ƽ����*/
    double *centers_average_dist;   /**< Kmeans��������ĵ����������ƽ��ֵ*/
    double *max_sample_id;
    double *max_sample_dist;
    u_int *centers_update_num;     /**< Kmeans��������ĵ���´���*/
    double *projection_vector;      /**< Kmeans��������ͶӰ������*/
    double *projection_dist;        /**< Kmeans��������ĵ�����ͶӰֵ*/
    int *projection_centers_id;     /**< Kmeans��������ĵ�����ͶӰֵ������*/
} kmeans_model_t;


typedef struct _mutil_thread_node{
    u_int start;                    /**< ���߳������ĵ�һ��������*/
    u_int end;                      /**< ���߳����������һ��������*/
    kmeans_dataset_t *data;         /**< ���߳�������� : �����ڴ���������Ϣ*/
    kmeans_conf_t *conf;            /**< ���߳�������� : ������Ϣ*/
    kmeans_model_t *model;          /**< ���߳�������� : �������ĵ���Ϣ*/
} thread_node;

//-----------------------��ȡ������Ϣ����------------------------------
/**
 * @brief ���help��Ϣ
 * @param [in] argv[0]
 * no return
 * */
void usage(const char *program_name);
/**
 * @brief �����в�����ȡ
 * @param [in] argc,*argv :     �����в�����Ϣ
 * @param [in] conf_fname :     �����ļ���ַ
 * @param [in] samples_fname :  ������Ϣ�ļ���ַ
 * @param [in] cluster_conf :   �����ļ��ṹ��
 * return int
 *      -1  ��ȡ����ʧ��
 *      1   ��ȡ�����ɹ�
 * */
int cluster_parse_args(int argc, char *argv[], char *&conf_fname, char *&samples_fname, kmeans_conf_t *cluster_conf);
/**
 * @brief �����в�����ȡ
 * @param [in] conf_fname :     �����ļ���ַ
 * @param [in] conf :           �����ļ��ṹ��
 * return int
 *      -1  ��ȡ�����ļ�ʧ��
 *      1   ��ȡ�����ļ��ɹ�
 * */
int cluster_read_conf(const char *conf_fname, kmeans_conf_t *conf);

//-----------------------����ģ�麯���ӿ�------------------------------
/**
 * @brief ���ĵ��ļ���Ϣ����
 * @param [in] model:           ����ģ��
 * @param [in] conf :           �����ļ��ṹ��
 * return int
 *      -1  �������ĵ���Ϣʧ��
 *      1   �������ĵ���Ϣ�ɹ�
 * */
int centers_load(kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief Ԥ�����޳�����Ҫʹ�õ�������
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  Ԥ����ʧ��
 *      1   Ԥ����ɹ�
 * */
int preprocess(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief ��ʼ��K�����ĵ�
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  ���ĵ��ʼ��ʧ��
 *      1   ���ĵ��ʼ���ɹ�
 * */
int init_k_centers(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief ��Ӳ����ѡ����Ҫ����ѵ��������
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * return int
 *      -1  ѡ�������ɹ�
 *      1   ѡ������ʧ��
 * */
int samples_choose(kmeans_dataset_t *data, kmeans_conf_t *conf);
/**
 * @brief ����samples_choose()��Ӳ������������
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] samples_fname :  ѵ��������Ϣ�ļ�
 * return int
 *      -1  ��������ʧ��
 *      1   ��������ɹ�
 * */
int data_load(char *samples_fname, kmeans_dataset_t *data, kmeans_conf_t *conf);
/**
 * @brief ѡ�������������
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * @param [in] left_iter :      ��ʣ��������
 * return int
 *      -1  ����ѡ��ʧ��
 *      1   ����ѡ��ɹ�
 * */
int next_samples_choose(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief Ϊ���������ҵ���������ĵ�
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  �������ʧ��
 *      1   ������ڳɹ�
 * */
int nearest_node(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief �������ĵ�
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  ���ĵ����ʧ��
 *      1   ���ĵ���³ɹ�
 * */
int centers_update(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model, double
&max_epilson, u_int &rand_num);
/**
 * @brief ���ļ������������ҵ���������ĵ�
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  ʧ��
 *      1   �ɹ�
 * */
int line_to_center(char *samples_fname, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief ����������ĵ���Ϣ
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  ʧ��
 *      1   �ɹ�
 * */
int centers_info_out(kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief ���������������Ϣ
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  ʧ��
 *      1   �ɹ�
 * */
int samples_result(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief ��ʼ��һ������ģ��
 * @param [in] conf :           �����ļ��ṹ��
 * return kmeans_model_t *
 *      NULL    ʧ��
 *      other   ����ģ��ָ��
 * */
kmeans_model_t *centers_created( kmeans_conf_t *conf);
/**
 * @brief ��ʼ��һ����������ģ��
 * @param [in] conf :           �����ļ��ṹ��
 * return kmeans_model_t *
 *      NULL    ʧ��
 *      other   ����ģ��ָ��
 * */
kmeans_dataset_t * data_created(kmeans_conf_t *conf);
/**
 * @brief Ϊ�û������key�ҵ���������������
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  ʧ��
 *      1   �ɹ�
 * */
int KNN_get_center(kmeans_model_t *model, kmeans_conf_t *conf, kmeans_dataset_t *data);
/**
 * @brief Ϊ�û������key�������������ֵ�����k����
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  ʧ��
 *      1   �ɹ�
 * */
int KNN_samples_result(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);
/**
 * @brief �ͷ���ռ���ڴ�
 * @param [in] data :           ������������
 * @param [in] conf :           �����ļ��ṹ��
 * @param [in] model :          ����ģ��
 * return int
 *      -1  ʧ��
 *      1   �ɹ�
 * */
int free_strcut(kmeans_dataset_t *data, kmeans_conf_t *conf, kmeans_model_t *model);


#endif  //__MY_CLUSTER_H_
/* vim: set expandtab ts=4 sw=4 sts=4 tw=100: */
