/***************************************************************************
 * 
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * 
 **************************************************************************/
 
 
 
/**
 * @file CKMKmeans_helper.h
 * @author dongdaxiang@baidu.com
 * @date 2012/05/08 19:58:33
 * @brief helper functions for client implementation.
 *  
 **/

#ifndef CKMKmeans_HELPER_H__
#define CKMKmeans_HELPER_H__
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <stdio.h>
#include <stdlib.h>
using std::map;
using std::string;
using namespace std;
map<string, bool> CMD_LINE_BOOLS;
map<string, float> CMD_LINE_FLOATS;
map<string, int> CMD_LINE_INTS;
map<string, string> CMD_LINE_STRINGS;
map<string, string> CMD_LINE_DESCRIPTIONS;

int CKM_add_flag(const string & flag_name,
                 const string & description,
                 bool default_value)
{
  if (CMD_LINE_DESCRIPTIONS.find(flag_name) != CMD_LINE_DESCRIPTIONS.end())
    {
      std::cerr << "Error. " << flag_name << " appears more than once. " << std::endl;
      return -1;
    }
  CMD_LINE_DESCRIPTIONS[flag_name] = description;
  CMD_LINE_BOOLS[flag_name] = default_value;
  return 0;
}

int CKM_add_flag(const string & flag_name,
                 const string & description,
                 float default_value)
{
  if (CMD_LINE_DESCRIPTIONS.find(flag_name) != CMD_LINE_DESCRIPTIONS.end())
    {
      std::cerr << "Error. " << flag_name << " appears more than once. " << std::endl;
      return -1;
    }
  CMD_LINE_DESCRIPTIONS[flag_name] = description;
  CMD_LINE_FLOATS[flag_name] = default_value;
  return 0;
}

int CKM_add_flag(const string & flag_name,
            const string & description,
            int default_value)
{
  if (CMD_LINE_DESCRIPTIONS.find(flag_name) != CMD_LINE_DESCRIPTIONS.end())
    {
      std::cerr << "Error. " << flag_name << " appears more than once. " << std::endl;
      return -1;
    }
  CMD_LINE_DESCRIPTIONS[flag_name] = description;
  CMD_LINE_INTS[flag_name] = default_value;
  return 0;
}

int CKM_add_flag(const string & flag_name,
            const string & description,
            string default_value)
{
  if (CMD_LINE_DESCRIPTIONS.find(flag_name) != CMD_LINE_DESCRIPTIONS.end())
    {
      std::cerr << "Error. " << flag_name << " appears more than once. " << std::endl;
      return -1;
    }
  CMD_LINE_DESCRIPTIONS[flag_name] = description;
  CMD_LINE_STRINGS[flag_name] = default_value;
  return 0;
}

void CKM_show_help()
{
  std::cout << std::endl;
  std::cout << "Command line flag options: " << std::endl;
  std::cout << "-------------------------------------------------------------------------------------" << std::endl;
  for (map<string, string>::iterator iter = CMD_LINE_DESCRIPTIONS.begin();
       iter != CMD_LINE_DESCRIPTIONS.end();
       iter++)
    {
      fprintf(stderr, "     %-20s", iter->first.c_str());
      fprintf(stderr, "  %s\n", iter->second.c_str());
    }
  std::cout << std::endl;
  std::cout << "------------------------------------------------------------------------------------" << std::endl;
  exit(0);
}

bool CKM_parse_bool_flag(char ** argv, int * i)
{
  if (CMD_LINE_BOOLS.find(argv[*i]) != CMD_LINE_BOOLS.end())
    {
      CMD_LINE_BOOLS[argv[*i]] = true;
      ++(*i);
      return true;
    }
  return false;
}

bool CKM_parse_general_flag(int argc, char ** argv, int * i)
{
  if (CMD_LINE_FLOATS.find(argv[*i]) != CMD_LINE_FLOATS.end() ||
      CMD_LINE_INTS.find(argv[*i]) != CMD_LINE_INTS.end() ||
      CMD_LINE_STRINGS.find(argv[*i]) != CMD_LINE_STRINGS.end())
    {
      if (*i + 1 >= argc || (argv[*i + 1])[0] == '-')
        {
          std::cerr << "Error. " << argv[*i] << " needs a value, but is given none. "
                    << std::endl;
          return false;
        }
      std::stringstream arg_stream(argv[(*i + 1)]);
      if (CMD_LINE_FLOATS.find(argv[*i]) != CMD_LINE_FLOATS.end())
        {
          float value;
          arg_stream >> value;
          CMD_LINE_FLOATS[argv[*i]] = value;
          *i += 2;
          return true;
        }
      if (CMD_LINE_INTS.find(argv[*i]) != CMD_LINE_INTS.end())
        {
          int value;
          arg_stream >> value;
          CMD_LINE_INTS[argv[*i]] = value;
          *i += 2;
          return true;
        }
      if (CMD_LINE_STRINGS.find(argv[*i]) != CMD_LINE_STRINGS.end())
        {
          string value;
          arg_stream >> value;
          CMD_LINE_STRINGS[argv[*i]] = value;
          *i += 2;
          return true;
        }      
    }
  return false;
}

int CKM_parse_flags(int argc, char ** argv)
{
  if (argc == 1) CKM_show_help();
  int i = 1;
  while (i < argc)
    {
      bool good_parse = false;
      good_parse = good_parse || CKM_parse_bool_flag(argv, &i);
      good_parse = good_parse || CKM_parse_general_flag(argc, argv, &i);
      if (!good_parse)
        {
          std::cerr << "Error. " << argv[i] << " is not a valid flag." << std::endl;
          return -1;
        }
    }
  return 0;
}

#endif
