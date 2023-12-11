#include <iostream>
#include <string>
#include <vector>
#include <windows.h>
#include <sql.h>
#include <sqlext.h>
#include <sqltypes.h>
#include <tchar.h>
#include <fstream>
#include <sstream>

#include <Winuser.h>
#include <winuser.h>
#include <commctrl.h>

#pragma comment(lib, "odbc32.lib")

HICON hIcon;

LRESULT CALLBACK WindowProcedure(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInst, HINSTANCE hPrevInst, LPSTR args, int ncmdshow) {
    WNDCLASSW wc = { 0 };
    wc.hbrBackground = (HBRUSH)COLOR_WINDOW;
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hInstance = hInst;
    wc.lpszClassName = L"myWindowClass";
    wc.lpfnWndProc = WindowProcedure;

    if (!RegisterClassW(&wc))
        return -1;

    CreateWindowW(L"myWindowClass", L"HHM_MSSQL", WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        0, 0, 800, 600, NULL, NULL, NULL, NULL);

    MSG msg = { 0 };

    while (GetMessage(&msg, NULL, NULL, NULL))
    {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

LRESULT CALLBACK WindowProcedure(HWND hWnd, UINT msg, WPARAM wp, LPARAM lp) {
    switch (msg)
    {
    case WM_CREATE:
    {
        HMENU hMenubar = CreateMenu();
        HMENU hFile = CreateMenu();
        HMENU hEdit = CreateMenu();

        AppendMenu(hMenubar, MF_POPUP, (UINT_PTR)hFile, L"File");
        AppendMenu(hMenubar, MF_POPUP, (UINT_PTR)hEdit, L"Edit");

        AppendMenu(hFile, MF_STRING, 1, L"Exit");

        SetMenu(hWnd, hMenubar);

        HWND hServerLabel = CreateWindowW(L"static", L"Server:", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            20, 20, 100, 25, hWnd, (HMENU)NULL, NULL, NULL);
        HWND hServerEntry = CreateWindowW(L"edit", L"", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            130, 20, 200, 25, hWnd, (HMENU)NULL, NULL, NULL);

        HWND hDBLabel = CreateWindowW(L"static", L"Database:", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            20, 50, 100, 25, hWnd, (HMENU)NULL, NULL, NULL);
        HWND hDBEntry = CreateWindowW(L"edit", L"", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            130, 50, 200, 25, hWnd, (HMENU)NULL, NULL, NULL);

        HWND hUsernameLabel = CreateWindowW(L"static", L"Username:", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            20, 80, 100, 25, hWnd, (HMENU)NULL, NULL, NULL);
        HWND hUsernameEntry = CreateWindowW(L"edit", L"", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            130, 80, 200, 25, hWnd, (HMENU)NULL, NULL, NULL);

        HWND hPasswordLabel = CreateWindowW(L"static", L"Password:", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            20, 110, 100, 25, hWnd, (HMENU)NULL, NULL, NULL);
        HWND hPasswordEntry = CreateWindowW(L"edit", L"", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            130, 110, 200, 25, hWnd, (HMENU)NULL, NULL, NULL);

        HWND hTestButton = CreateWindowW(L"button", L"Test Connection", WS_CHILD | WS_VISIBLE | WS_BORDER,
            350, 20, 150, 25, hWnd, (HMENU)1, NULL, NULL);

        HWND hSaveButton = CreateWindowW(L"button", L"Save Configuration", WS_CHILD | WS_VISIBLE | WS_BORDER,
            350, 50, 150, 25, hWnd, (HMENU)2, NULL, NULL);

        HWND hOpenQueryButton = CreateWindowW(L"button", L"Open Query Library", WS_CHILD | WS_VISIBLE | WS_BORDER,
            350, 80, 150, 25, hWnd, (HMENU)3, NULL, NULL);

        HWND hQueryLabel = CreateWindowW(L"static", L"Query:", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT,
            20, 150, 100, 25, hWnd, (HMENU)NULL, NULL, NULL);
        HWND hQueryEntry = CreateWindowW(L"edit", L"", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_MULTILINE,
            130, 150, 550, 150, hWnd, (HMENU)NULL, NULL, NULL);

        HWND hExecuteButton = CreateWindowW(L"button", L"Execute", WS_CHILD | WS_VISIBLE | WS_BORDER,
            350, 310, 150, 25, hWnd, (HMENU)4, NULL, NULL);

        HWND hResultList = CreateWindowW(L"listbox", L"", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_AUTOVSCROLL,
            20, 350, 760, 150, hWnd, (HMENU)NULL, NULL, NULL);

        HWND hResultText = CreateWindowW(L"edit", L"", WS_CHILD | WS_VISIBLE | WS_BORDER | ES_LEFT | ES_AUTOVSCROLL,
            20, 510, 760, 25, hWnd, (HMENU)NULL, NULL, NULL);

        HWND hExportButton = CreateWindowW(L"button", L"Export Excel", WS_CHILD | WS_VISIBLE | WS_BORDER,
            350, 550, 150, 25, hWnd, (HMENU)5, NULL, NULL);
    }
    break;

    case WM_COMMAND:
    {
        if (wp == 1)
        {
            MessageBoxW(hWnd, L"Test Connection button clicked", L"Info", MB_OK);
        }
        else if (wp == 2)
        {
            MessageBoxW(hWnd, L"Save Configuration button clicked", L"Info", MB_OK);
        }
        else if (wp == 3)
        {
            MessageBoxW(hWnd, L"Open Query Library button clicked", L"Info", MB_OK);
        }
        else if (wp == 4)
        {
            MessageBoxW(hWnd, L"Execute button clicked", L"Info", MB_OK);
        }
        else if (wp == 5)
        {
            MessageBoxW(hWnd, L"Export Excel button clicked", L"Info", MB_OK);
        }
    }
    break;

    case WM_DESTROY:
        PostQuitMessage(0);
        break;

    default:
        return DefWindowProcW(hWnd, msg, wp, lp);
    }
}

