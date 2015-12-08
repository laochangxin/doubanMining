/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
/**
 * @file CKMNMF.h
 * @author dongdaxiang@baidu.com
 * @date 2012/12/26 19:58:33
 * @brief header file for non negative matrix factorzation
 *  
 **/

#ifndef NMF_H_
#define NMF_H_

typedef struct CKM_nmf_
{
    unsigned k;
    unsigned m;
    unsigned n;
    double ** W;
    double ** H;
    unsigned * membership;
    char ** row_map;
    char ** col_map;
} CKM_nmf_model_t;

typedef struct CKM_nmf_pred_
{
    int k;
    int m;
    int n;
    double ** F;
    int * membership;
    char ** row_map;
} CKM_nmf_pred_t;

extern CKM_nmf_model_t * CKM_nmf_learn_model(char * filename, unsigned k);

extern int CKM_nmf_free_model(CKM_nmf_model_t ** model);

extern int CKM_nmf_save_model(CKM_nmf_model_t * model, char * foldername);

extern CKM_nmf_model_t * CKM_nmf_load_model(char * folder);

//extern CKM_nmf_pred_t * CKM_nmf_get_factor(char * filename);

//extern int CKM_nmf_free_factor(CKM_nmf_pred_t ** pred);

#endif
