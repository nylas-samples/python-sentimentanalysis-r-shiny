library("shiny")
library("tidyverse")
library("treemap")
library("imager")
library("plyr")

ui <- fluidPage(
  tags$div(
    HTML("<h1 style='color:blue;text-align:center;'>VeggiEggs Dashboard!</h1>")
  ),  
  title = "VeggiEggs Dashboard!",
                 fluidRow(
                   column(width=5, plotOutput(outputId = "distPlot")),
                   column(width=5,offset=2, plotOutput(outputId = "distPlot2"))
                 ),
                 fluidRow(
                   column(width=5, plotOutput(outputId = "distPlot3")),
                   column(width=5,offset=2, plotOutput(outputId = "distPlot4"))
                 )) 


server <- function(input, output) {
  args = commandArgs(trailingOnly=TRUE)
  ratings<-as.integer(strsplit(args[1], ",")[[1]])
  sentiments<-strsplit(args[2], ",")[[1]]
  scores<-as.integer(strsplit(args[3], ",")[[1]])    
  dates<-as.Date(strsplit(args[4], ",")[[1]])
  
  entries = data.frame(ratings, sentiments, scores, dates=as.Date(dates))  
  
  output$distPlot <- renderPlot({
    Ratings <- count(entries, 'ratings')
    names(Ratings)<-c("Ratings","Count")
    Count <- Ratings$Count
    Ratings %>%
      ggplot( aes(x = Ratings, y = Count, fill = Count)) + 
        geom_bar(stat="identity")
  })
  
  output$distPlot2 <- renderPlot({
    Freq <- count(entries, 'dates')
    names(Freq)<-c("Dates","Entries")
    Freq %>% 
      ggplot( aes(x=Dates, y=Entries)) +
      geom_line(color="green") +
      geom_point()
  })
  
  output$distPlot3 <- renderPlot({
    Sentiment <- count(sentiments)
    group <- paste(Sentiment$x,Sentiment$freq)
    sentiment<-Sentiment$freq
    data <- data.frame(group,sentiment)
    treemap(data,
            index="group",
            vSize="sentiment",
            type="index"
    )
  })
  
  output$distPlot4 <- renderPlot({
    Score<-mean(entries$scores)
    if (Score < -0.5){
      image_filename<-"angry-emoji.png"
    }
    if (Score > -0.5 && Score < 0.5){
      image_filename<-"neutral-emoji.png"
    }
    if (Score > 0.5){
      image_filename<-"happy-emoji.jpeg"
    }
    
    image <- load.image(image_filename)
    plot(image)
  })
  
}

shinyApp(ui = ui, server = server)
