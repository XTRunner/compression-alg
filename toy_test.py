import compress_methods

def main():
    test_array = [5, 2, 2, 4, 1, 1, 0, 2, 6, 13, 6, 8, 7, 0, 0, 6, 1, 0, 0, 8, 9, 4, 2, 2,
                  6, 1, 18, 3, 1, 4, 0, 1, 6, 8, 5, 20, 2, 2, 3, 2, 0, 3, 0, 0, 0, 1, 9,
                  11, 3, 5, 2, 2, 1, 2, 0, 4, 1, 9, 1, 14, 5, 4, 4, 2, 2, 0, 0, 0, 1, 2, 4,
                  4, 5, 0, 1, 9, 1, 0, 0, 0, 3, 10, 27, 20, 15, 4, 0, 1, 0, 1, 0, 0, 8, 18]
    c_tools = compress_methods.compress(test_array)
    dp_res = c_tools.modify_dp(2)
    vw_res = c_tools.modify_vw(20)
    opt_res = c_tools.modify_opt(2)
    print(dp_res)
    print(vw_res)
    print(opt_res)


if __name__ == "__main__":
    main()
