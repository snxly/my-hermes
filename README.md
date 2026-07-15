# my-hermes

Hermes Agent 配置文件管理。

## 结构

```
profiles/
├── default/        ~/.hermes/config.yaml + .env
├── cook/
├── dev/
├── dev-lead/
├── pm/
├── qa-engineer/
├── reviewer/
└── todo-master/
```

每个 profile 的 `config.yaml` 和 `.env` 通过软链接指向此仓库，
修改后 `git commit` 即可追溯历史。

## 工作流

```bash
# 编辑配置
vim profiles/default/config.yaml

# 提交变更
git add profiles/default/config.yaml
git commit -m "config(default): 改模型为 deepseek-v4-flash"
git push
```
