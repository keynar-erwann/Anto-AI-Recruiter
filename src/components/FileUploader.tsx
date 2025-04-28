import React, { useState, useRef } from 'react';
import { Upload, XCircle, FileText, Image, File } from 'lucide-react';

interface FileUploaderProps {
  onFilesSelected: (files: File[]) => void;
}

const FileUploader: React.FC<FileUploaderProps> = ({ onFilesSelected }) => {
  const [files, setFiles] = useState<File[]>([]);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      const newFiles = Array.from(event.target.files);
      setFiles(prev => [...prev, ...newFiles]);
      onFilesSelected([...files, ...newFiles]);
    }
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    
    if (event.dataTransfer.files) {
      const newFiles = Array.from(event.dataTransfer.files);
      setFiles(prev => [...prev, ...newFiles]);
      onFilesSelected([...files, ...newFiles]);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const removeFile = (index: number) => {
    const newFiles = [...files];
    newFiles.splice(index, 1);
    setFiles(newFiles);
    onFilesSelected(newFiles);
  };

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    if (extension === 'pdf') return <FileText className="h-5 w-5 text-red-500" />;
    if (['jpg', 'jpeg', 'png'].includes(extension || '')) return <Image className="h-5 w-5 text-blue-500" />;
    if (extension === 'docx') return <File className="h-5 w-5 text-indigo-500" />;
    return <File className="h-5 w-5 text-gray-500" />;
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-5 mb-6 transition-all hover:shadow-lg">
      <div className="flex items-center mb-3">
        <Upload className="h-5 w-5 text-indigo-600 mr-2" />
        <h3 className="text-lg font-medium text-gray-800">Transférez les CVs</h3>
      </div>
      
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-all ${
          isDragging ? 'border-indigo-500 bg-indigo-50' : 'border-gray-300 hover:border-indigo-400'
        }`}
        onClick={() => fileInputRef.current?.click()}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        <input
          type="file"
          multiple
          onChange={handleFileChange}
          accept=".pdf,.docx,.jpg,.jpeg,.png"
          className="hidden"
          ref={fileInputRef}
        />
        <Upload className="h-10 w-10 text-indigo-400 mx-auto mb-3" />
        <p className="text-gray-700 mb-1 font-medium">Déposez vos fichiers ici ou cliquez pour parcourir</p>
        <p className="text-gray-500 text-sm">Formats acceptés: PDF, DOCX, JPG, PNG</p>
      </div>
      
      {files.length > 0 && (
        <div className="mt-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Fichiers sélectionnés:</h4>
          <ul className="space-y-2 max-h-40 overflow-y-auto">
            {files.map((file, index) => (
              <li key={index} className="flex items-center justify-between bg-gray-50 p-2 rounded-md transition-all hover:bg-gray-100">
                <div className="flex items-center">
                  {getFileIcon(file.name)}
                  <span className="ml-2 text-sm text-gray-700 truncate max-w-xs">{file.name}</span>
                </div>
                <button
                  className="text-gray-400 hover:text-red-500 transition-colors"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(index);
                  }}
                >
                  <XCircle className="h-5 w-5" />
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default FileUploader;