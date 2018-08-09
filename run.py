# -*- coding: utf-8 -*-

import argparse
from bot import pre


def get_parser():
    parser = argparse.ArgumentParser(description='Bot que monitora o controle academico no período de matriculas '
                                                 'e avisa quando as matriculas são abertas!')
    parser.add_argument("-m", "--matricula", help='matrícula do aluno, ex: 117896523')
    parser.add_argument("-s", "--senha", nargs='+', help='senha do aluno')
    return parser


def command_line_runner():
    parser = get_parser()
    args = vars(parser.parse_args())
    enrolment = args['matricula']
    password = args['senha']
    if enrolment and password:
        pre.start_bot(enrolment, password)
    elif not enrolment or not password:
        print("Você precisa passar a matricula e senha, meu anjo! use o --help para mais informações :)")
    else:
        parser.print_help()


if __name__ == '__main__':
    command_line_runner()
