import killbilllib as kbf

# killbil V.0.1


def main():
    # kbf.killbill()
    kbf.deleteDataFiles(delmsg=False)
    kbf.active_window()
    kbf.getProcessesInfo()

    # if 'y' == input('\n___do you want to use recommended exceptional processes (y/n):   '):
        # print('\nWe terminated all background processes')
    try:
        kbf.terminateProcessess()
    except(Exception) as e:
        print(e)
    finally:
        kbf.deleteDataFiles(True)

    # else:
    #     if 'y' == input('\ndo you have exceptional processes (y/n):   '):
    #         kbf.editExceptionalProcesses()
    #         print('\n____hmm that\'s fine we use these settings___')
    #     else:
    #         print('\n___Okay that\'s fine we use recommended exceptional processes :)___')
    #     kbf.terminateProcessess()
    #     kbf.deleteDataFiles(True)

    # print('done')


if __name__ == "__main__":
    main()
