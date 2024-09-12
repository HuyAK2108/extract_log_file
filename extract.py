import logging
import argparse
import os

def parse_opt():
  """Options or Arguments input from users

  Returns:
      argparse: 
  """
  parser = argparse.ArgumentParser(description='Extract grep keyword')
  parser.add_argument("-d", '--debug', action= 'store_true', help="log level debug")
  parser.add_argument("-i", action= 'store_true', help="grep both lower and upper")
  parser.add_argument("-f", '--file', nargs="+", help="file path", default='run_dir/run.log')
  parser.add_argument("-o", '--output', help="output file path", default='DEBUG.log')
  parser.add_argument("-l", '--list', nargs="+", help="<Required> Set flag", default=['EVENT_CHK', 'CCX0_RAS', 'CCX1_RAS', 'CCS_PMU', 'CCX0_PMU', 'CCX1_PMU'])
  opt = parser.parse_args()
  return opt

def list_log_files(directory):
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.endswith(".log"):
        run_log = os.path.join(root, file)
        logging.debug(f'Reading {run_log}')
        return run_log

def read_log_file(opt):
  """Read input log file

  Args:
      opt (argparse): options input from users

  Returns:
      text: returns text read from log file
  """
  text = ""
  count = 0
  try:
    for index, list in enumerate(opt.file):
      run_log = list_log_files(list)
      # Open single run.log file
      with open(run_log, "r") as file:
        for line in file:
          if opt.list:
            for i, kw in enumerate(opt.list):
              # Grep both lower and upper case
              if opt.i:
                if str(kw) in line.lower():
                  if count == 0:
                    text  += f'\n-----{run_log}-----\n'
                    count += 1
                  text += f'{line.strip()}\n'
              # Grep exact case
              else:
                if str(kw) in line:
                  if count == 0:
                    text  += f'\n-----{run_log}-----\n'
                    count += 1
                  text += f'{line.strip()}\n'
      count = 0

      # Warning when there is no str
      if text == "":
        logging.warning(f'There is no "{opt.list}" in "{run_log}"')

    # Print text in log level debug    
    logging.debug('%s', text)
    
    print(f'Done reading {opt.file}')
    return text
  except Exception as e:
    print(f'Error occurred when opening {opt.file} to read: {e}')
    return None

def print_output(dest_file, content):
  """function print file out

  Args:
      dest_file (str): file out path
      content (str): contents contain keyword

  Returns:
      Bool: True if write successfullu, else None
  """
  try:
    f = open(dest_file, "w")
    f.write(content)
    f.close()
    return True
  except Exception as e:
    print(f'Error occurred when opening {dest_file} to read: {e}')
    return False

def main(opt):
  if opt.debug:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
  
  content = read_log_file(opt= opt)
  
  if content == "":
    print(f"Done extract without generate output")
  elif content == None:
    print("ERROR")
  else:
    if (print_output(opt.output, content)):
      print(f'Write Successfully to {opt.output}')

if __name__ == '__main__':
  opt = parse_opt()
  main(opt=opt)