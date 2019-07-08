#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, time, os, subprocess, time, shutil, json

testcases = [
    ('data/prime_1.in', 'data/prime_1.out'),
    ('data/prime_2.in', 'data/prime_2.out'),
    ('data/prime_3.in', 'data/prime_3.out'),
    ('data/prime_4.in', 'data/prime_4.out'),
    ('data/prime_5.in', 'data/prime_5.out'),
    ('data/prime_6.in', 'data/prime_6.out'),
    ('data/prime_7.in', 'data/prime_7.out'),
    ('data/prime_8.in', 'data/prime_8.out'),
    ('data/prime_9.in', 'data/prime_9.out'),
    ('data/prime_10.in', 'data/prime_10.out'),
]

if __name__ == '__main__':

    if sys.version_info[0] != 3:
        print("Please use python3")
        exit(1)

    program_file = 'prime.py'
    if len(sys.argv) > 1: 
        program_file = sys.argv[1]
    
    if not os.path.isfile(program_file):
        print('File {} not present!'.format(program_file))
        exit(1)

    success_count = 0

    for input, output in testcases:
        # remove the output file
        test_filename = 'test.output'
        try:
            os.remove(test_filename)
        except:
            pass
        p = subprocess.Popen([sys.executable, program_file], stdin=open(input, 'r'), stdout=open(test_filename,'w'), stderr=open(os.devnull,'w'))
        message = ''
        success = True
        start_time = time.time()
        while p.poll() is None:
            if time.time() - start_time > 2:
                p.terminate()
                message = 'Time limit exceeded'
                success = False
                break
        else:
            if not os.path.isfile(test_filename):
                message = 'No output file found'
                success = False
            else:
                std = [line.strip() for line in open(output, 'r').readlines() if line.strip()]
                ans = [line.strip() for line in open(test_filename, 'r').readlines() if line.strip()]
                if len(std) != len(ans):
                    message = 'Line count mismatch'
                    success = False
                else:
                    for i in range(len(std)):
                        if std[i] != ans[i]:
                            message = 'Line {} mismatch: should be \'{}\', get \'{}\''.format(i, std[i], ans[i])
                            success = False
                            break
        if success:
            success_count += 1
            if os.isatty(1):
                print('Testcase {}: PASS'.format(input))
        else:
            if os.isatty(1):
                print('Testcase {}: {}'.format(input, message))
        
        
    grade = int(100.0 * success_count / len(testcases))
    
    if os.isatty(1):
        print('Total Points: {}/100'.format(grade))
    else:
        print(json.dumps({'grade': grade}))

