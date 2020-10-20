from mini_editor.shell import run, compile

compile("""
#include<stdio.h>
#include<conio.h>

int main(){
    int a;
	printf("Enter Number:");
	scanf("%d",&a);
	getch();
}
""")
run()
