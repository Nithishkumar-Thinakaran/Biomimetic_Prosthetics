# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



    # Use a breakpoint in the code line below to debug your script.





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
n=54321
rn=0
while n>0:
    digit=n%10
    rn=rn*10+digit
    n//=10
print(rn)