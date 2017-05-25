#ifndef EXTRACTOR_H
#define EXTRACTOR_H

#include <QObject>

class Extractor : public QObject
{
    Q_OBJECT
public:
    explicit Extractor(QObject *parent = 0);
    void start_extract();

signals:

public slots:

private:
    void create_idfile(QString filename);

};

#endif // EXTRACTOR_H
