local status, colorizer = pcall(require, "colorizer")

if (not status) then return end
--
-- colorizer.setup({
--   '*';
-- })
--
-- Attaches to every FileType mode
colorizer.setup()
