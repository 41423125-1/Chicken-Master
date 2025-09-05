# pip install PyGithub
# conda install -c conda-forge pygithub
from github import Github, Auth, InputFileContent

# GitHub 個人 token
auth = Auth.Token("your_github_token")
g = Github(auth=auth)

# 取得當前使用者
user = g.get_user()

# 建立 Gist（需用 InputFileContent）
gist = user.create_gist(
    public=True,
    files={
        "Readme.txt": InputFileContent(content="#Readme")
    },
    description="空白 Gist 倉儲"
)
# 取得 Gist ID
gist_id = gist.id

print("Gist ID:", gist_id)
# 假設 "gist" 為 Putty 設定專用於 Gist 的 session 名稱
print("Git clone URL (SSH):", f"git@gist:{gist_id}.git")
print("HTML URL:", gist.html_url)

