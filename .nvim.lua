local lint = require("lint")

local new_args = { "--rcfile", "./backend/.pylintrc" }
for _, item in ipairs(new_args) do
	table.insert(lint.linters.pylint.args, item)
end

local lspconfig = require("lspconfig")
lspconfig.pyright.setup({
	settings = {
		python = {
			analysis = {
				typeCheckingMode = "strict",
			},
		},
	},
})
