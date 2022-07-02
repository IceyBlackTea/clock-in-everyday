'''
Author: IceyBlackTea
Date: 2021-11-05 10:30:32
LastEditors: IceyBlackTea
LastEditTime: 2022-07-02 11:06:30
FilePath: /clock-in-everyday/auto_clock_in.py
Description: Copyright © 2021 IceyBlackTea. All rights reserved.
'''

# encoding:utf-8
import utils


def clock_in(config):
    try:
        flag = False

        while True:
            hour = utils.get_local_hour()

            if not flag and hour > 9:
                content = 'have not clock in yet!'
                utils.print_logs(content)

                if config['send_mail']:
                    utils.send_mail(config['mail_config'], 'Oh No', content)
                
            if flag and hour != 1:
                utils.wait_until_next_hour()
                continue

            flag = False

            try:
                token, headers = utils.sign_in(config['baidu_ocr'], config['sign_in_config'])

            except Exception as e:
                utils.handle_error(e)

            else:
                try:
                    clock_in_config = config['clock_in_config'][config['type_']]
                    utils.clock_in(clock_in_config, token, headers)

                except Exception as e:
                    utils.handle_error(e)
                    
                else:
                    flag = True
                    
                    content = 'Time to sleep!'

                    if config['send_mail']:
                        utils.send_mail(config['mail_config'], 'Clock In', content)
                        
                    utils.wait_until_next_hour()

    except KeyboardInterrupt:
        utils.print_logs('Stopped by Keyboard. Bye!')


def main():
    clock_in(utils.get_config())


if __name__ == '__main__':
    main()


