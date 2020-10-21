from mini_editor.shell import c_run, c_compile

c_compile("""
#include<stdio.h>
#include<conio.h>

int main(){
    int a;
	printf("Enter Number:");
	scanf("%d",&a);
	getch();
}
""")
c_run(["start", "./a.exe"])
