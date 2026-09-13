#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<algorithm>
#include<cstdlib>
#include<ctime>
using namespace std;
struct Question
{
    string question;
    string op1;
    string op2;
    string op3;
    string op4;
    int answer;
};
string currentUser = "";

void registerUser();
bool loginUser();
bool adminLogin();

void studentMenu();
void adminMenu();

void addQuestion();
void viewQuestions();
void deleteQuestion();

void startQuiz();
void saveResult(string username, int score, int total);
void viewResults();

int main()
{
    int choice;

    while(true)
    {
        cout<<"\n=====================================\n";
        cout<<"      QUIZ MANAGEMENT SYSTEM\n";
        cout<<"=====================================\n";

        cout<<"1. Student Registration\n";
        cout<<"2. Student Login\n";
        cout<<"3. Admin Login\n";
        cout<<"4. Exit\n";

        cout<<"\nEnter Choice : ";

while(!(cin >> choice))
{
    cin.clear();
    cin.ignore(1000, '\n');
    cout<<"Invalid Input! Enter Again: ";
}

        switch(choice)
        {
            case 1:
                registerUser();
                break;

            case 2:
                if(loginUser())
                    studentMenu();
                else
                    cout<<"\nInvalid Username or Password\n";
                break;

            case 3:
                if(adminLogin())
                    adminMenu();
                else
                    cout<<"\nWrong Admin Credentials\n";
                break;

            case 4:
            {
               char ch;

               cout<<"\nAre you sure you want to exit? (Y/N): ";
               cin>>ch;

               if(ch=='Y' || ch=='y')
                {
                  cout<<"\nThank You For Using Quiz Management System.\n";
                  return 0;
            }

    break;
}

            default:
                cout<<"\nInvalid Choice\n";
        }
    }
}

void registerUser()
{
    string user,pass;

    cout<<"\nUsername : ";
    cin>>user;

    cout<<"Password : ";
    cin>>pass;

    ofstream file("users.txt",ios::app);

    file<<user<<" "<<pass<<endl;

    file.close();

    cout<<"\nRegistration Successful\n";
}

bool loginUser()
{
    string user,pass;
    string u,p;

    cout<<"\nUsername : ";
    cin>>user;

    cout<<"Password : ";
    cin>>pass;

    ifstream file("users.txt");

    while(file>>u>>p)
    {
       if(user==u && pass==p)
{
    currentUser = user;
    file.close();
    return true;
}
    }

    file.close();
    return false;
}

bool adminLogin()
{
    string user,pass;
    string u,p;

    cout<<"\nAdmin Username : ";
    cin>>user;

    cout<<"Password : ";
    cin>>pass;

    ifstream file("admin.txt");

    while(file>>u>>p)
    {
        if(user==u && pass==p)
        {
            file.close();
            return true;
        }
    }

    file.close();

    return false;
}

void studentMenu()
{
    int choice;

    while(true)
    {
        cout<<"\n================================\n";
        cout<<"        STUDENT PANEL\n";
        cout<<"================================\n";

        cout<<"1. Start Quiz\n";
        cout<<"2. View Previous Results\n";
        cout<<"3. Logout\n";

        cout<<"\nEnter Choice : ";

while(!(cin >> choice))
{
    cin.clear();
    cin.ignore(1000, '\n');
    cout<<"Invalid Input! Enter Again: ";
}

        switch(choice)
        {
            case 1:
                startQuiz();
                break;

            case 2:
                viewResults();
                break;

            case 3:
                return;

            default:
                cout<<"\nInvalid Choice\n";
        }
    }
}

void adminMenu()
{
    int choice;

    while(true)
    {
        cout<<"\n================================\n";
        cout<<"          ADMIN PANEL\n";
        cout<<"================================\n";

        cout<<"1. Add Question\n";
        cout<<"2. View Questions\n";
        cout<<"3. Delete Question\n";
        cout<<"4. Logout\n";

        cout<<"\nEnter Choice : ";

while(!(cin >> choice))
{
    cin.clear();
    cin.ignore(1000, '\n');
    cout<<"Invalid Input! Enter Again: ";
}

        switch(choice)
        {
            case 1:
                addQuestion();
                break;

            case 2:
                viewQuestions();
                break;

            case 3:
                deleteQuestion();
                break;

            case 4:
                return;

            default:
                cout<<"\nInvalid Choice\n";
        }
    }
}

void addQuestion()
{
    ofstream file("questions.txt", ios::app);

    string question;
    string op1, op2, op3, op4;
    int answer;

    cin.ignore();

    cout<<"\nEnter Question : ";
    getline(cin, question);

    cout<<"Option 1 : ";
    getline(cin, op1);

    cout<<"Option 2 : ";
    getline(cin, op2);

    cout<<"Option 3 : ";
    getline(cin, op3);

    cout<<"Option 4 : ";
    getline(cin, op4);

    cout<<"Correct Option (1-4): ";
    cin>>answer;

    file<<question<<endl;
    file<<op1<<endl;
    file<<op2<<endl;
    file<<op3<<endl;
    file<<op4<<endl;
    file<<answer<<endl;

    file.close();

    cout<<"\nQuestion Added Successfully.\n";
}

void viewQuestions()
{
    ifstream file("questions.txt");

    if(!file)
    {
        cout<<"\nNo Questions Available.\n";
        return;
    }

    string question, op1, op2, op3, op4;
    int answer;

    int count = 1;

    cout<<"\n========== QUESTIONS ==========\n";

    while(getline(file, question))
    {
        getline(file, op1);
        getline(file, op2);
        getline(file, op3);
        getline(file, op4);
        file>>answer;
        file.ignore();

        cout<<"\nQuestion "<<count++<<endl;

        cout<<question<<endl;
        cout<<"1. "<<op1<<endl;
        cout<<"2. "<<op2<<endl;
        cout<<"3. "<<op3<<endl;
        cout<<"4. "<<op4<<endl;
        cout<<"Answer : "<<answer<<endl;
    }

    file.close();
}

void deleteQuestion()
{
    ifstream file("questions.txt");

    if(!file)
    {
        cout<<"\nNo Questions Available.\n";
        return;
    }

    vector<string> data;

    string question, op1, op2, op3, op4;
    int ans;

    while(getline(file, question))
    {
        getline(file, op1);
        getline(file, op2);
        getline(file, op3);
        getline(file, op4);
        file >> ans;
        file.ignore();

        data.push_back(question);
        data.push_back(op1);
        data.push_back(op2);
        data.push_back(op3);
        data.push_back(op4);
        data.push_back(to_string(ans));
    }

    file.close();

    int total = data.size() / 6;

    if(total == 0)
    {
        cout<<"\nNo Questions Found.\n";
        return;
    }

    cout<<"\nAvailable Questions\n";

    for(int i=0;i<total;i++)
    {
        cout<<i+1<<". "<<data[i*6]<<endl;
    }

    int del;

    cout<<"\nEnter Question Number to Delete : ";
    cin>>del;

    if(del<1 || del>total)
    {
        cout<<"\nInvalid Choice\n";
        return;
    }

    ofstream out("questions.txt");

    for(int i=0;i<total;i++)
    {
        if(i==del-1)
            continue;

        out<<data[i*6]<<endl;
        out<<data[i*6+1]<<endl;
        out<<data[i*6+2]<<endl;
        out<<data[i*6+3]<<endl;
        out<<data[i*6+4]<<endl;
        out<<data[i*6+5]<<endl;
    }

    out.close();

    cout<<"\nQuestion Deleted Successfully.\n";
}

void startQuiz()
{
    ifstream file("questions.txt");

    if(!file)
    {
        cout<<"\nNo Questions Available.\n";
        return;
    }

    vector<Question> quiz;

    Question q;

    while(getline(file,q.question))
    {
        getline(file,q.op1);
        getline(file,q.op2);
        getline(file,q.op3);
        getline(file,q.op4);

        file>>q.answer;
        file.ignore();

        quiz.push_back(q);
    }

    file.close();

    if(quiz.size()==0)
    {
        cout<<"\nNo Questions Found.\n";
        return;
    }

    srand(time(0));

    random_shuffle(quiz.begin(),quiz.end());

    int score=0;

    cout<<"\n========== QUIZ ==========\n";

    for(int i=0;i<quiz.size();i++)
    {
        cout<<"\nQuestion "<<i+1<<endl;

        cout<<quiz[i].question<<endl;

        cout<<"1. "<<quiz[i].op1<<endl;
        cout<<"2. "<<quiz[i].op2<<endl;
        cout<<"3. "<<quiz[i].op3<<endl;
        cout<<"4. "<<quiz[i].op4<<endl;

        int ans;

        while(true)
        {
            cout<<"Your Answer (1-4): ";
            cin>>ans;

            if(ans>=1 && ans<=4)
                break;

            cout<<"Invalid Option! Try Again.\n";
        }

        if(ans==quiz[i].answer)
            score++;
    }

    cout<<"\n================================\n";

    cout<<"Quiz Completed\n";

    cout<<"Score : "<<score<<"/"<<quiz.size()<<endl;

    float per=((float)score/quiz.size())*100;

    cout<<"Percentage : "<<per<<"%\n";

    if(per>=80)
        cout<<"Grade : A\n";
    else if(per>=60)
        cout<<"Grade : B\n";
    else if(per>=40)
        cout<<"Grade : C\n";
    else
        cout<<"Grade : FAIL\n";

    saveResult(currentUser,score,quiz.size());
}
void saveResult(string username,int score,int total)
{
    ofstream file("results.txt",ios::app);

    file<<username<<" "
        <<score<<"/"<<total
        <<endl;

    file.close();
}



void viewResults()
{
    ifstream file("results.txt");

    if(!file)
    {
        cout<<"\nNo Results Found.\n";
        return;
    }

    string user;
    string marks;

    cout<<"\n=====================================\n";
    cout<<"           LEADERBOARD\n";
    cout<<"=====================================\n";

    cout<<"Username\tScore\n";
    cout<<"-----------------------------\n";

    while(file>>user>>marks)
    {
        cout<<user<<"\t\t"<<marks<<endl;
    }

    file.close();

    cout<<"-----------------------------\n";
}

void startQuiz();
void saveResult(string username, int score, int total);
void viewResults();