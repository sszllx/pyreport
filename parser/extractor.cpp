#include "extractor.h"

#include <QCoreApplication>
#include <QDir>
#include <QDebug>
#include <QFile>
#include <QTextStream>
#include <QTimer>

void Extractor::create_idfile(QString filename)
{
  QFile infile(filename);
  QString out_filename;
  int id_count = 0;

  out_filename = filename.replace(".log", ".id");
  QFile outfile(out_filename);
  QTextStream out(&outfile);

  if (!infile.open(QIODevice::ReadOnly | QIODevice::Text)) {
      qDebug() << "infile open failed";
      return;
  }

  if (!outfile.open(QIODevice::WriteOnly | QIODevice::Text)) {
      qDebug() << "outfile open failed";
      return;
  }

  quint64 file_size = infile.size();
  quint64 summary_size = 0;

  while (!infile.atEnd()) {
    QString data = infile.read(4096);
    int index = 0;
    int totalLen = data.size();

    summary_size += totalLen;
    qDebug() << "complete: " << (double)((double)summary_size/(double)file_size)*100;

    while ((index = data.indexOf("idfa", index)) > 0) {
      QStringList ids;
      if (index + 42 >= totalLen) {
        index = totalLen - index;
        quint64 pos = infile.pos();
        infile.seek(pos - index - 2);
        break;
      }

      index += 7;

      QString id = data.mid(index, 36);
      // out << id << "\n";
//      bool same = false;
//      foreach (QString str, ids) {
//        if (str == id) {
//            same = true;
//            break;
//        }
//      }

      if (id != "00000000-0000-0000-0000-000000000000") {
//          ids << id;
          out << id << "\n";
      }

//      const char *ch = id.toStdString().c_str();

//      printf("%d %s", id_count++, ch);
//      printf("\r\033[k");
    }
  }
}


Extractor::Extractor(QObject *parent) : QObject(parent)
{

}

void Extractor::start_extract()
{
    QString cur_dir = QCoreApplication::applicationDirPath() + "/ioslogs/";
    qDebug() << "cur dir:" << cur_dir;
    QDir dir(cur_dir);
    QStringList filter;
    filter << "*.log";
    QFileInfoList list = dir.entryInfoList(filter, QDir::Files);

    for (int i = 0; i < list.size(); ++i) {
        QFileInfo fileInfo = list.at(i);
        qDebug() << fileInfo.absoluteFilePath();
        create_idfile(fileInfo.absoluteFilePath());
        QFile file(fileInfo.absoluteFilePath());
        // file.remove();
    }

    QTimer::singleShot(1000*60*15, this, &Extractor::start_extract);
}
