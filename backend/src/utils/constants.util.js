const ALLOWED_FILES_TABLES = ['video_calls', 'tablets_knox', 'tablets_nexus', 'citizens'];
const ALLOWED_FILE_EXT = ['csv'];
const ALLOWED_MIME_TYPES = ['text/csv'];
const MAX_FILE_SIZE = 2;

module.exports = {
    ALLOWED_FILES_TABLES,
    ALLOWED_FILE_EXT,
    ALLOWED_MIME_TYPES,
    MAX_FILE_SIZE,
}